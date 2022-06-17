import time
import numpy as np

from math import dist
from fastapi import File, UploadFile, APIRouter, HTTPException
from pathlib import Path
from service.retrieval.crawler.crawler_process import crawl
from service import (
    read_csv_file,
    read_pkl_file,
    handle_uploaded_image,
    get_model_predicted_results,
    FeatureExtractor,
)
from dotenv import load_dotenv
from os import environ as ENV

load_dotenv()

# Create Fast API route instance
router = APIRouter()

# Declare Rarible NFT Market api url
NFT_API_URL = "https://api.rarible.org/v0.1/items"


# Declare loaded full-features array
full_features_path = ENV.get("FEATURES_FULL_PATH")

# Declare loaded pca-features array
pca_features_path = ENV.get("FEATURES_PCA_PATH")

# Declare loaded image token array
tokens_path = ENV.get("TOKEN_PATH")

num_of_result = int(ENV.get("NUM_OF_RESULT"))


# Create new feature extractor instance to extract image

# Read images from extracted folder and load to arrays
## Note: each token, filename, features vector is identified by the order in the array
full_features = read_pkl_file(full_features_path)
pca_features = read_pkl_file(pca_features_path)
tokens = read_pkl_file(tokens_path)

feature_extractor = FeatureExtractor(
    vector_features_full=full_features,
    vector_features_pca=pca_features,
    vector_tokens=tokens,
    num_of_return=num_of_result,
)


# POST image api
@router.post("/api/v1/upload")
async def post_image(file: UploadFile = File(...)):
    try:
        # Read content of uploaded image
        contents = await file.read()
        # Handle and save uploaded image
        image, uploaded_image_path = handle_uploaded_image(contents, file)
        #  Executed model start time
        start = time.time()

        result = feature_extractor.search(uploaded_image_path)

        #  Executed model end time
        end = time.time()

        # Calculate and print out executed time
        print(f"Runtime of the searching is {end - start}")

        # Get top similar item from model and return result from NFT market api

        start = time.time()
        responses = get_model_predicted_results(result, NFT_API_URL)
        end = time.time()
        print(f"Runtime of the retrieve is {end - start}")

    except Exception as exception:
        # Catch error
        raise HTTPException(status_code=404, detail=exception)
    finally:
        return {"result": responses}


@router.get("/api/v1/crawl")
async def get_collection():
    try:
        crawl()
    except Exception as exception:
        raise HTTPException(status_code=404, detail=exception)

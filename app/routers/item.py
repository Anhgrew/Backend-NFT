import time
import numpy as np
from starlette.requests import Request
from math import dist
from fastapi import File, UploadFile, APIRouter, HTTPException, Depends
from pathlib import Path
import io
from PIL import Image
from sklearn import feature_extraction
from service.file_handle import load_pickle_file
from service.retrieval.crawler.crawler_process import crawl
from service import (
    read_csv_file,
    read_pkl_file,
    handle_uploaded_image,
    get_model_predicted_results,
    FeatureExtractor,
)
from core.config import settings
from dotenv import load_dotenv
from os import environ as ENV

from starlette.concurrency import run_in_threadpool

load_dotenv()

# Create Fast API route instance
router = APIRouter()

# Declare Rarible NFT Market api url
NFT_API_URL = "https://api.rarible.org/v0.1/items"


# Declare loaded full-features array
FEATURES_PATH = settings.FEATURES_PATH

# Declare loaded image token array
TOKENS_PATH = settings.TOKENS_PATH

NUM_OF_RESULT = settings.NUM_OF_RESULT


# Create new feature extractor instance to extract image

# Read images from extracted folder and load to arrays
## Note: each token, filename, features vector is identified by the order in the array
full_features = load_pickle_file(FEATURES_PATH)
tokens = load_pickle_file(TOKENS_PATH)


feature_extractor = {}
feature_extractor = FeatureExtractor(
    vector_features_full=full_features,
    vector_tokens=tokens,
    num_of_return=NUM_OF_RESULT,
)


# POST image api
@router.post("/api/v1/upload")
async def upload_image(data: bytes = File(...)):
    try:
        # Read content of uploaded image
        img_search = Image.open(io.BytesIO(data)).convert("RGB")

        #  Executed model start time
        start = time.time()

        result = feature_extractor.search(img=img_search)

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


async def parse_body(request: Request):
    data: bytes = await request.body()
    return data


@router.post("/api/v2/upload")
async def post_image(data: bytes = Depends(parse_body)):
    try:
        # Read content of uploaded image
        img_search = Image.open(io.BytesIO(data)).convert("RGB")

        #  Executed model start time
        start = time.time()

        result = feature_extractor.search(img=img_search)

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


@router.get("/api/v1/crawl/amount/{num_of_collections}")
async def get_collection(num_of_collections: int):
    try:
        await run_in_threadpool(crawl, num_of_collections)
        
    except Exception as exception:
        raise HTTPException(status_code=404, detail=exception)

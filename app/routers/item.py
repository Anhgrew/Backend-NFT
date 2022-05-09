import time
import numpy as np

from math import dist
from fastapi import File, UploadFile, APIRouter, HTTPException
from pathlib import Path
from service import read_csv_file, read_pkl_file, handle_uploaded_image, get_model_predicted_results, FeatureExtractor

# Create Fast API route instance 
router = APIRouter()

# Declare Rarible NFT Market api url
NFT_API_URL = "https://api.rarible.org/v0.1/items"


# Create new feature extractor instance to extract image
feature_extractor = FeatureExtractor()
# Declare loaded images array
feature_pkl_path = 'vector_pca.pkl'
features = []
# Declare loaded images path array
path_pkl_path = 'paths_pca.pkl'
img_paths = []
# Declare loaded image token array
token_pkl_path = 'token_pca.pkl'
nft_tokens = []

# Read images from extracted folder and load to arrays
## Note: each token, filename, features vector is identified by the order in the array
features = read_pkl_file(feature_pkl_path)
img_paths = read_pkl_file(path_pkl_path)
nft_tokens = read_pkl_file(token_pkl_path)

# POST image api
@router.post("/api/v1/upload")
async def post_image(file: UploadFile = File(...)):
    try:
        # Read content of uploaded image
        contents = await file.read()
        # Handle and save uploaded image
        image = handle_uploaded_image(contents, file)
        #  Executed model start time
        start = time.time()

        # Extract query uploaded image
        query = feature_extractor.extract(image)

        # L2 distances to features
        dists = np.linalg.norm(features - query, axis=1)

        # Top 10 most similar images id
        ids = np.argsort(dists)[:10]

        #  Executed model end time
        end = time.time()

        # Calculate and print out executed time
        print(f"Runtime of the searching is {end - start}")

        # Get top similar item from model and return result from NFT market api
        responses = get_model_predicted_results(ids, nft_tokens, NFT_API_URL)
        
    except Exception as exception:
        # Catch error
        raise HTTPException(status_code=404, detail=exception)
    finally:
        return {'result': responses}

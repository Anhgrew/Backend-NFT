import time
import numpy as np

from math import dist
from fastapi import File, UploadFile, APIRouter, HTTPException
from pathlib import Path
from service import read_csv_file, handle_uploaded_image, get_model_predicted_results, FeatureExtractor

# Create Fast API route instance 
router = APIRouter()

# Declare Rarible NFT Market api url
NFT_API_URL = "https://api.rarible.org/v0.1/items"

# Read image paths in csv file
nft_address_map = read_csv_file("./static/DataAddress.csv")

# Create new feature extractor instance to extract image
feature_extractor = FeatureExtractor()
# Declare loaded images array
features = []
# Declare loaded images path array
img_paths = []

# Read images from extracted folder and load to arrays
for feature_path in Path("./static/feature").glob("*.npy"):
    features.append(np.load(feature_path))
    img_paths.append(Path("./static/Data") / (feature_path.stem + ".png"))
features = np.array(features)

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

        # Top 5 most similar images
        ids = np.argsort(dists)[:5]

        #  Executed model end time
        end = time.time()

        # Calculate and print out executed time
        print(f"Runtime of the searching is {end - start}")

        # Get index of most similar image with folder path
        scores = [(dists[id], img_paths[id]) for id in ids]
        # Get top similar item from model and return result from NFT market api
        responses = get_model_predicted_results(scores, nft_address_map, NFT_API_URL)
        
    except Exception as exception:
        # Catch error
        raise HTTPException(status_code=404, detail=exception)
    finally:
        return {'result': responses}

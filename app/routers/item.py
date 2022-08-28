import time
from fastapi import File, APIRouter, HTTPException
import io
from PIL import Image
from service.file_handle import load_pickle_file
from service.feature_extractor import FeatureExtractor
from core.config import settings
from database.db import ShoeDatabase


# Create Fast API route instance
router = APIRouter()

# Declare loaded full-features array
FEATURES_PATH = settings.FEATURES_PATH

# Declare loaded image token array
TOKENS_PATH = settings.TOKENS_PATH

NUM_OF_RESULT = settings.NUM_OF_RESULT

shoe_repos = ShoeDatabase()

# Create new feature extractor instance to extract image
# Read images from extracted folder and load to arrays
## Note: each token, filename, features vector is identified by the order in the array

full_features = load_pickle_file(FEATURES_PATH)
tokens = load_pickle_file(TOKENS_PATH)

print("loaded image: ", len(full_features))
print("loaded token: ", len(tokens))

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
        responses = shoe_repos.get_model_predicted_results(result)
        end = time.time()
        print(f"Runtime of the retrieve is {end - start}")

    except Exception as exception:
        # Catch error
        raise HTTPException(status_code=404, detail=exception)
    finally:
        return {"result": responses}

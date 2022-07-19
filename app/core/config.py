from pydantic import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    app_name: str = "User Api"
    FEATURES_PATH: str
    TOKENS_PATH: str
    NUM_OF_RESULT: int

    ITEMS_API: str
    ITEMS_STORAGE: str
    COLLECTIONS_STORAGE: str
    COLLECTIONS_TO_UPDATE: str
    TOP_COLLECTION_API: str
    ITEM_BY_IDS_API: str
    IMAGE_ACCEPTED_TYPES: list
    MAX_ITEMS: int

    class Config:
        env_file = ".env"


settings = Settings()

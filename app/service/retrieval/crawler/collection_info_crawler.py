import requests
from dotenv import load_dotenv
from os import environ as ENV

load_dotenv()
from service.retrieval.crawler.crawler_file_handle import (
    write_crawler_file,
    read_crawler_file,
)


# Get collections ID
collection_api = ENV["COLLECTION_API"]
collection_storage = ENV.get("COLLECTION_STORAGE")
collection_to_update = ENV.get("COLLECTION_TO_UPDATE")
collection_to_delete = ENV.get("COLLECTION_TO_DELETE")

collections_id = {}


def get_collections_id():
    collection_request = requests.get(collection_api)
    collection_raw = collection_request.json()
    for id, collection_item in enumerate(collection_raw):
        collections_id[str(id)] = collection_item["id"]


def update_collection_id():
    # load
    deleting_item = {}
    current_items = read_crawler_file(collection_storage)
    # process
    write_crawler_file(collection_to_update, collections_id)
    for key, item in current_items.items():
        if not item in collections_id.values():
            deleting_item[key] = item
    print(len(deleting_item))
    write_crawler_file(collection_to_delete, deleting_item)

import requests
from service.retrieval.crawler.url_modify import UrlModify
from core.config import settings
from os import environ as ENV

from service.retrieval.crawler.crawler_file_handle import (
    write_crawler_file,
    read_crawler_file,
    append_crawler_file,
)


# Get collections ID
COLLECTION_API = settings.TOP_COLLECTION_API
COLLECTIONS_STORAGE = settings.COLLECTIONS_STORAGE
COLLECTIONS_TO_UPDATE = settings.COLLECTIONS_TO_UPDATE

collections_id = dict()


def get_collections_id(num_of_collections):
    """
        get collection the most famous list from COLLECTION_API
    """
    collection_downloaded = read_crawler_file(COLLECTIONS_STORAGE)
    downloaded_list = list(collection_downloaded.values())

    num_of_downloaded = int(len(collection_downloaded))
    num_of_get = num_of_downloaded + int(num_of_collections)
    url = UrlModify(top=num_of_get).get_url()

    collection_request = requests.get(url)
    collection_raw = collection_request.json()

    set_collections = set()

    for _, collection_item in enumerate(collection_raw):
        set_collections.add(collection_item["id"])

    pending_list = list(set_collections)
    pending_list = [item for item in pending_list if item not in downloaded_list]
    pending_list = pending_list[:num_of_collections]
    for i, item in enumerate(pending_list):
        collections_id[str(i)] = item


def update_collections_id():
    write_crawler_file(COLLECTIONS_TO_UPDATE, collections_id)
    collections_id.clear()

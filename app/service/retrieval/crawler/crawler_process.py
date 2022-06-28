import requests
import os
import os.path as pth

from service.retrieval.crawler.collection_info_crawler import *
from service.retrieval.crawler.item_info_crawler import *
from service.retrieval.crawler.crawler_process import *
from service.retrieval.crawler.item_extractor import *

from dotenv import load_dotenv
from os import environ as ENV

load_dotenv()

# Update storage
ITEMS_STORAGE = ENV.get("ITEMS_STORAGE")
COLLECTIONS_STORAGE = ENV.get("COLLECTIONS_STORAGE")
COLLECTIONS_TO_UPDATE = ENV.get("COLLECTIONS_TO_UPDATE")


def update_collection_info():
    """
        Update information from collection_to_update list
    """
    collections_list = read_crawler_file(COLLECTIONS_TO_UPDATE)
    for collection_id in collections_list.values():
        get_collection_info(collection_id)


def update_record():
    update_list = read_crawler_file(COLLECTIONS_TO_UPDATE)
    write_crawler_file(COLLECTIONS_STORAGE, update_list)
    write_crawler_file(COLLECTIONS_TO_UPDATE, {})


def crawl(num_of_collections):
    # print("stage 1")
    get_collections_id(num_of_collections)
    # print("stage 2")
    update_collections_id()
    # print("stage 3")
    update_collection_info()
    # print("stage 4")
    update_record()
    # print("stage 5")
    extract_all()
    # print("end")

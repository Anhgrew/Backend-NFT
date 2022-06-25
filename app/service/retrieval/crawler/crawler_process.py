import requests
import os
import os.path as pth
import csv

from service.retrieval.crawler.collection_info_crawler import *
from service.retrieval.crawler.item_info_crawler import *
from service.retrieval.crawler.crawler_process import *
from service.retrieval.crawler.item_extractor import *

from dotenv import load_dotenv
from os import environ as ENV

load_dotenv()

# Update storage
item_storage = ENV.get("ITEM_STORAGE")
collection_storage = ENV.get("COLLECTION_STORAGE")
collection_to_update = ENV.get("COLLECTION_TO_UPDATE")
collection_to_delete = ENV.get("COLLECTION_TO_DELETE")


def update_collection_info():
    collections_list = read_crawler_file(collection_to_update)
    for collection_id in collections_list.values():
        get_collection_info(collection_id)


def delete_collection_info():
    collections_list = read_crawler_file(collection_to_delete)
    for collection_id in collections_list.values():
        if pth.exists(item_storage + collection_id):
            os.remove(item_storage + collection_id)


def update_record():
    update_list = read_crawler_file(collection_to_update)
    write_crawler_file(collection_storage, update_list)
    write_crawler_file(collection_to_update, {})
    write_crawler_file(collection_to_delete, {})


def crawl():
    get_collections_id()
    update_collection_id()
    update_collection_info()
    delete_collection_info()
    update_record()
    extract_all()

import sys
import requests
import os
import os.path as pth
from service.retrieval.crawler.crawler_file_handle import (
    write_crawler_file,
    read_crawler_file,
)
from core.config import settings
from os import environ as ENV


ITEMS_API = settings.ITEMS_API
ITEMS_STORAGE = settings.ITEMS_STORAGE
CURRENCY = "ETHEREUM:"
IMAGE_ACCEPTED_TYPES = settings.IMAGE_ACCEPTED_TYPES
IMAGE_EXTENSION_ACCEPTED = [".jpg", ".jpeg", ".png"]
MAX_ITEMS = int(settings.MAX_ITEMS)


def extract_item_info(item_json):
    try:
        content = item_json["meta"]["content"]
    except:
        return [item_json["id"], ""]
    smallest = sys.maxsize
    url = ""
    for item in content:
        if str(item.get("mimeType")) in IMAGE_ACCEPTED_TYPES:
            if item.get("size"):
                url = item["url"] if item["size"] < smallest else url
            elif url == "":
                url = item["url"]
        if url == "":
            for ext in IMAGE_EXTENSION_ACCEPTED:
                if ext in item["url"]:
                    url = item["url"]
    return item_json["id"], url


def get_collection_info(token_id):
    count = 0
    address_book = dict()
    signal = ""
    if pth.exists(ITEMS_STORAGE + token_id + "/address_book.csv"):
        current_data = read_crawler_file(ITEMS_STORAGE + token_id + "/address_book.csv")
        print(CURRENCY + token_id)
        print(len(current_data))
        return
    while count < MAX_ITEMS:
        # get collection
        collection_request = requests.get(
            ITEMS_API,
            params={"collection": CURRENCY + token_id, "continuation": signal},
        )
        while not collection_request.status_code == 200:
            collection_request = requests.get(
                ITEMS_API,
                params={"collection": CURRENCY + token_id, "continuation": signal},
            )
        result_raw = collection_request.json()

        # get item
        result_items = result_raw["items"]
        for item_info in result_items:
            if item_info["id"] in address_book.keys():
                continue
            id, url = extract_item_info(item_info)
            if url != "":
                count += 1
                address_book[id] = url
            if count == MAX_ITEMS:
                break

        # check continuation
        next_signal = signal
        if "continuation" in result_raw:
            next_signal = result_raw["continuation"]
        if next_signal == signal or next_signal == "" or next_signal in address_book:
            break
        signal = next_signal

    # saving
    if not pth.exists(ITEMS_STORAGE + token_id):
        os.makedirs(ITEMS_STORAGE + token_id)
    write_crawler_file(ITEMS_STORAGE + token_id + "/address_book.csv", address_book)
    print(CURRENCY + token_id)
    print(len(address_book))

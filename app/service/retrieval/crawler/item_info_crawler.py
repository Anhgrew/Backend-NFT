import requests
import os
import os.path as pth

from service.retrieval.crawler.crawler_file_handle import (
    write_crawler_file,
    read_crawler_file,
)

from dotenv import load_dotenv
from os import environ as ENV

load_dotenv()

item_api = "https://api.rarible.org/v0.1/items/byCollection"
item_storage = ENV.get("ITEM_STORAGE")
currency = "ETHEREUM:"


def extract_item_info(item_json):
    extracted_item = [item_json["id"], ""]
    if "meta" in item_json:
        if len(item_json["meta"]["content"]) > 0:
            if item_json["meta"]["content"][0]["@type"] == "IMAGE":
                if "url" in item_json["meta"]["content"][0]:
                    extracted_item = [
                        item_json["id"],
                        item_json["meta"]["content"][0]["url"],
                    ]
    return extracted_item


def get_collection_info(token_id):
    address_book = {}
    signal = ""
    if pth.exists(item_storage + token_id + "/address_book.csv"):
        current_data = read_crawler_file(item_storage + token_id + "/address_book.csv")
        print(currency + token_id)
        print(len(current_data))
        return
    while True:
        # get collection
        collection_request = requests.get(
            item_api, params={"collection": currency + token_id, "continuation": signal}
        )
        while not collection_request.status_code == 200:
            collection_request = requests.get(
                item_api,
                params={"collection": currency + token_id, "continuation": signal},
            )
        result_raw = collection_request.json()

        # get item
        result_items = result_raw["items"]
        for item_info in result_items:
            if item_info["id"] in address_book.keys():
                continue
            extracted_item = extract_item_info(item_info)
            address_book[extracted_item[0]] = extracted_item[1]

        # check continuation
        next_signal = signal
        if "continuation" in result_raw:
            next_signal = result_raw["continuation"]
        if next_signal == signal or next_signal == "" or next_signal in address_book:
            break
        signal = next_signal

    # saving
    if not pth.exists(item_storage + token_id):
        os.makedirs(item_storage + token_id)
    write_crawler_file(item_storage + token_id + "/address_book.csv", address_book)
    print(currency + token_id)
    print(len(address_book))

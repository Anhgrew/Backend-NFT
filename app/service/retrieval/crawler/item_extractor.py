import requests
import os
import os.path as pth
import PIL
from io import BytesIO
from service.feature_extractor import FeatureExtractor
from service.retrieval.crawler.crawler_file_handle import (
    write_crawler_file,
    read_crawler_file,
)
from dotenv import load_dotenv
from os import environ as ENV

load_dotenv()

item_storage = ENV["ITEM_STORAGE"]
extractor = FeatureExtractor()


def extract_by_link(img_url):
    img_data = requests.get(img_url, stream=True)
    img_pic = PIL.Image.open(img_data.raw).convert("RGB")
    vector_feature_extracted = extractor.extract(img=img_pic)
    return vector_feature_extracted


def extract_collection(collection_id):
    print(collection_id)
    storage_path = item_storage + "/" + collection_id
    if pth.exists(storage_path + "/data.csv"):
        return
    if not pth.exists(storage_path + "/address_book.csv"):
        return
    items_list = read_crawler_file(storage_path + "/address_book.csv")
    extracted_result = {}
    for key, value in items_list.items():
        extracted_result[key] = extract_by_link(value)
    write_crawler_file(storage_path + "/data.csv", extracted_result)
    print("done")


def extract_all():
    for path_id in os.listdir(item_storage):
        extract_collection(path_id)

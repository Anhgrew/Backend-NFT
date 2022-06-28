import requests
import os
import os.path as pth
import PIL
from service.feature_extractor import FeatureExtractor
from service.retrieval.crawler.crawler_file_handle import (
    write_crawler_file,
    read_crawler_file,
    write_pickle_file,
)
from dotenv import load_dotenv
from os import environ as ENV

load_dotenv()

ITEMS_STORAGE = ENV["ITEMS_STORAGE"]
extractor = FeatureExtractor()


def extract_by_link(img_url):
    img_data = requests.get(img_url, stream=True)
    img_pic = PIL.Image.open(img_data.raw).convert("RGB")
    vector_feature_extracted = extractor.extract(img=img_pic)
    return vector_feature_extracted


def extract_collection(collection_id):
    storage_path = ITEMS_STORAGE + "/" + collection_id
    if pth.exists(storage_path + "/data.csv"):
        return
    if not pth.exists(storage_path + "/address_book.csv"):
        return
    items_list = read_crawler_file(storage_path + "/address_book.csv")
    extracted_result = dict()
    for key, value in items_list.items():
        extracted_result[key] = extract_by_link(value)

    print("write to pickle file")
    write_pickle_file(storage_path + "/key.pkl", list(extracted_result.keys()))
    write_pickle_file(storage_path + "/vectors.pkl", list(extracted_result.values()))
    print("done")


def extract_all():
    for path_id in os.listdir(ITEMS_STORAGE):
        extract_collection(path_id)

import requests
import os
import os.path as pth
import PIL
import pickle
from service.feature_extractor import FeatureExtractor
from service.retrieval.crawler.crawler_file_handle import (
    write_crawler_file,
    read_crawler_file,
    write_pickle_file,
    append_crawler_file,
)
from dotenv import load_dotenv
from os import environ as ENV

load_dotenv()

ITEMS_STORAGE = ENV["ITEMS_STORAGE"]
VECTOR_TOKEN_ID_PKL = ENV["VECTOR_TOKEN_ID_PKL"]
VECTOR_FEATURES_PKL = ENV["VECTOR_FEATURES_PKL"]

extractor = FeatureExtractor()


def extract_by_link(img_url):
    img_data = requests.get(img_url, stream=True)
    img_pic = PIL.Image.open(img_data.raw).convert("RGB")
    vector_feature_extracted = extractor.extract(img=img_pic)
    return vector_feature_extracted


def extract_collection(collection_id):
    storage_path = ITEMS_STORAGE + collection_id
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
    pickle.dump(list(extracted_result.keys()), open(VECTOR_TOKEN_ID_PKL, "ab+"))
    pickle.dump(list(extracted_result.values()), open(VECTOR_FEATURES_PKL, "ab+"))
    print("done")


def extract_all():
    collections_list = read_crawler_file(COLLECTIONS_TO_UPDATE)
    for collection_id in collections_list.values():
        extract_collection(collection_id)

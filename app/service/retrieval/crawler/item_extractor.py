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
)
from dotenv import load_dotenv
from core.config import settings

ITEMS_STORAGE = settings.ITEMS_STORAGE
VECTOR_TOKEN_ID_PKL = settings.TOKENS_PATH
VECTOR_FEATURES_PKL = settings.FEATURES_PATH
COLLECTIONS_TO_UPDATE = settings.COLLECTIONS_TO_UPDATE

extractor = FeatureExtractor()


def extract_by_link(img_url, list_rm =[], key = ''):
    try:
        img_data = requests.get(img_url, stream=True)
        while not img_data.status_code == 200:
            img_data = requests.get(
                img_data = requests.get(img_url, stream=True),
        )
        img_pic = PIL.Image.open(img_data.raw).convert("RGB")
        vector_feature_extracted = extractor.extract(img=img_pic)
        return vector_feature_extracted
    except Exception as e:
        print(e)
        list_rm.append(key)
        return ''



def extract_collection(collection_id):
    storage_path = ITEMS_STORAGE + collection_id
    if pth.exists(storage_path + "/data.csv"):
        return
    if not pth.exists(storage_path + "/address_book.csv"):
        return
    items_list = read_crawler_file(storage_path + "/address_book.csv")
    extracted_result = dict()
    count = 0
    list_rm = []
    for key, value in items_list.items():
        extracted_result[key] = extract_by_link(value, list_rm, key)
        count = count+1
        print(str(count) + ' items extracted', end = "\r")
    print(str(count) + ' items extracted')
    count_rm = 0
    for val in list_rm:
        count_rm = count_rm + 1
        extracted_result.pop(val)
        print(str(count_rm) + ' items removed', end = "\r")
    print(str(count_rm) + ' items removed')
    print(str(len(extracted_result)) + ' items total')

    write_pickle_file(storage_path + "/key.pkl", list(extracted_result.keys()))
    write_pickle_file(storage_path + "/vectors.pkl", list(extracted_result.values()))
    pickle.dump(list(extracted_result.keys()), open(VECTOR_TOKEN_ID_PKL, "ab+"))
    pickle.dump(list(extracted_result.values()), open(VECTOR_FEATURES_PKL, "ab+"))


def extract_all():
    collections_list = read_crawler_file(COLLECTIONS_TO_UPDATE)
    for collection_id in collections_list.values():
        print('+ ' + collection_id)
        extract_collection(collection_id)

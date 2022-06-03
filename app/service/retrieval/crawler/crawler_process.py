import requests
import os
import os.path as pth
import csv

from service.retrieval.crawler import get_collection_id, update_collection_id, get_collection_info, write_crawler_file, read_crawler_file, extract_all

#Update storage
item_storage = '/content/drive/MyDrive/empty/Set/Crawler/Data/'
collection_storage = '/content/drive/MyDrive/empty/Set/Crawler/Current.csv'
collection_to_update = '/content/drive/MyDrive/empty/Set/Crawler/Waiting.csv'
collection_to_delete = '/content/drive/MyDrive/empty/Set/Crawler/Holding.csv'

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

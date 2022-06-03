import requests

from service.retrieval.crawler import write_crawler_file, read_crawler_file


#Get collections ID
collection_api = 'https://api-mainnet.rarible.com/marketplace/api/v4/collections/top?blockchains=ETHEREUM&days=1&size=30'
collection_storage = '/content/drive/MyDrive/empty/Set/Crawler/Current.csv'
collection_to_update = '/content/drive/MyDrive/empty/Set/Crawler/Waiting.csv'
collection_to_delete = '/content/drive/MyDrive/empty/Set/Crawler/Holding.csv'

collections_id = {}

def get_collections_id():
  collection_request = requests.get(collection_api)
  collection_raw = collection_request.json()
  for id, collection_item in enumerate(collection_raw):
    collections_id[str(id)] = collection_item['id']

def update_collection_id():
  #load
  deleting_item = {}
  current_items = read_crawler_file(collection_storage)
  #process
  write_crawler_file(collection_to_update, collections_id)
  for key, item in current_items.items():
    if not item in collections_id.values():
      deleting_item[key] = item
  print(len(deleting_item))
  write_crawler_file(collection_to_delete, deleting_item)

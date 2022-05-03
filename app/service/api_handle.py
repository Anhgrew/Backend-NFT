import requests


def get_nft_by_id(url, id):
    req = requests.get("/".join((url, id)))
    return req

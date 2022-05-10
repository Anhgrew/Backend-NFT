from service import get_nft_by_id
from models import Item

# Get top similar images and retrive more info from NFT market


def get_model_predicted_results(nft_tokens, market_url):
    responses = []
    for nft_token in nft_tokens:
        nft_req = get_nft_by_id(market_url, nft_token)
        response = nft_req.json()
        item = Item()
        item.id = response["id"]
        item.creators = response["creators"]
        item.owners = response["owners"]
        item.meta_name = response["meta"]["name"]
        item.meta_description = response["meta"]["description"]
        item.meta_content_url = response["meta"]["content"][0]["url"]
        if response.get("lastSale") is not None:
            item.lastsale_price = response["lastSale"]["price"]
        else:
            item.lastsale_price = "0"
        responses.append(item)

    return responses

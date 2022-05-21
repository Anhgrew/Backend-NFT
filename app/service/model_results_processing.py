from service import get_nft_by_id
from models import Item

# Get top similar images and retrive more info from NFT market


def get_model_predicted_results(nft_tokens, market_url):
    responses = []
    for nft_token in nft_tokens:
        nft_req = get_nft_by_id(market_url, nft_token)
        response = nft_req.json()
        item = Item()
        if "id" in response:
            item.id = response["id"]
        else:
            item.id = "?"
        if "creators" in response:
            item.creators = response["creators"]
        else:
            item.creators = "?"
        if "owners" in response:
            item.owners = response["owners"]
        else:
            item.owners = "?"
        if "meta" in response:
            sub_response = response["meta"]
            if "name" in sub_response:
                item.meta_name = response["meta"]["name"]
            else:
                item.meta_name = "?"
            if "description" in sub_response:
                item.meta_description = response["meta"]["description"]
            else:
                item.meta_description = "?"
            if "content" in sub_response:
                item.meta_content_url = response["meta"]["content"][0]["url"]
            else:
                item.meta_content_url = "?"
        if response.get("lastSale") is not None:
            item.lastsale_price = response["lastSale"]["price"]
        else:
            item.lastsale_price = "0"
        responses.append(item)

    return responses

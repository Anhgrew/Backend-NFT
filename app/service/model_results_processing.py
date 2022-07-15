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
            if "attributes" in sub_response:
                item.attributes = response["meta"]["attributes"]
            else:
                item.attributes = "?"
        else:
            item.meta_name = "?"
            item.meta_description = "?"
            item.meta_content_url = "?"
            item.attributes = "?"

        item.price = "-1"
        item.maker = "?"

        if response.get("bestSellOrder") is not None:
            _response = response["bestSellOrder"]
            if _response.get("take") is not None:
                _response = response["bestSellOrder"]["take"]
                if _response.get("value") is not None:
                    _response = response["bestSellOrder"]["take"]["value"]
                    item.price = _response
            _response = response["bestSellOrder"]
            if _response.get("maker") is not None:
                _response = response["bestSellOrder"]["maker"]
                item.maker = _response

        item.lastsale_price = "-1"
        
        if response.get("lastSale") is not None:
            _response = response["lastSale"]
            if _response.get("price") is not None:
                item.lastsale_price = response["lastSale"]["price"]

        responses.append(item)

    return responses
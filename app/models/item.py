from typing import List, Optional

# NFT item module
class Item():
    id: str
    creators: Optional[List[dict]] = []
    owners: Optional[List[str]] = []
    meta_name: Optional[str]
    meta_description: Optional[str]
    meta_content_url:  Optional[str]
    price:  Optional[str]
    lastsale_price:  Optional[str]
    attributes: Optional[str]
    maker: Optional[str]


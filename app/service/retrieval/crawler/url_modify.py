from urllib.parse import parse_qs, urlencode, urlparse, urlunparse
from core.config import settings
from os import environ as ENV


TOP_URL = settings.TOP_COLLECTION_API
DEFAULT_QUERY = {"blockchains": "ETHEREUM", "days": 1, "size": 4}


class UrlModify:
    def __init__(self, url=None, top=None, days=None) -> None:
        self.maximum = 100
        self.url = url if url else TOP_URL
        self.params = DEFAULT_QUERY
        self.params["days"] = days or self.params["days"]
        self.params["size"] = top or self.params["size"]
        self.params["size"] = 100 if top > 100 else self.params["size"]

    def get_url(self):
        url_parsed = urlparse(TOP_URL)
        query = parse_qs(url_parsed.query)
        query.update(self.params)
        encoded_query = urlencode(query)
        url_parsed = url_parsed._replace(query=encoded_query)
        new_url = urlunparse(url_parsed)
        return new_url


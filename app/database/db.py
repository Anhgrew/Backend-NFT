import json
from core.config import settings

# Get top similar images and retrive more info from NFT market
class ShoeDatabase:
    def __init__(self) -> None:
        self.path = settings.OBJECT_DATABASE
        self.database = self.load_database()
        return

    def load_database(self,):
        with open(self.path, "r") as data_file:
            data = json.loads(json.load(data_file))
        return data

    def get_model_predicted_results(self, ids):
        response = [self.database.get(str(id)) for id in ids]
        return response

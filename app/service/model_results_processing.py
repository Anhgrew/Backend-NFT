from database.db import shoe_repositories

def get_model_predicted_results(ids):
    return shoe_repositories.retrieve(ids)


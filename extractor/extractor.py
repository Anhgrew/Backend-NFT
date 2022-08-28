# import
import numpy as np
from numpy.linalg import norm
import pickle
from tqdm import tqdm, tqdm_notebook
import os
import time
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.applications.efficientnet import EfficientNetB4, preprocess_input

# from tensorflow.keras.applications.efficientnet import EfficientNetB4, preprocess_input
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors
import json
import requests
import PIL

"""
object format:
{
  _id : "1209380129204",
  name: "Hunter X1"
  image_url: "https://..."
}

mapping_format:
{
  image_url : _id
}
"""


class MyEffNetModel:
    def __init__(self, rank=10):
        self.model = EfficientNetB4(
            weights="imagenet",
            include_top=False,
            input_shape=(224, 224, 3),
            pooling="max",
        )
        self.my_data = []
        self.my_data_name = []
        self.rank = rank
        self.dataset = dict()

    def extract_features(self, img=None, img_path=None):
        input_shape = (224, 224, 3)
        target_size = (input_shape[0], input_shape[1])
        if img == None:
            img = image.load_img(path=img_path, target_size=target_size)
        else:
            img = img.resize(target_size)
        img_array = image.img_to_array(img)
        expanded_img_array = np.expand_dims(img_array, axis=0)
        preprocessed_img = preprocess_input(expanded_img_array)

        features = self.model.predict(preprocessed_img)
        flattened_features = features.flatten()
        normalized_features = flattened_features / norm(flattened_features)

        return normalized_features

    def extract_all_data(self):
        for img_url, img_id in self.dataset.items():
            img_data = requests.get(img_url, stream=True)
            img_pic = PIL.Image.open(img_data.raw).convert("RGB")
            self.my_data.append(self.extract_features(img=img_pic))
            self.my_data_name.append(img_id)

    def save(self, path="./"):
        pickle.dump(self.my_data, open(os.path.join(path, "key.pkl"), "wb"))
        pickle.dump(self.my_data_name, open(os.path.join(path, "vectors.pkl"), "wb"))

    """
        In this case, we using the json file with the image_url mapping with the object_id
    """

    def import_dataset(self, path):
        with open(path, "r") as json_file:
            self.dataset = json.loads(json.load(json_file))
        print(len(self.dataset))


extractor = MyEffNetModel()
extractor.import_dataset("./mapping.json")
extractor.extract_all_data()
extractor.save()

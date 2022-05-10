from pkg_resources import ExtractionError
from tensorflow.keras.preprocessing import image
from numpy.linalg import norm
import numpy as np

from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors

from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input


class FeatureExtractor:
    def __init__(self, vector_features, vector_tokens):
        self.init_model(vector_features, vector_tokens)
        self.init_pca()

    def init_model(self, vector_features, vector_tokens):
        self.model = ResNet50(
            weights="imagenet",
            include_top=False,
            input_shape=(224, 224, 3),
            pooling="max",
        )
        self.vector_features = vector_features
        self.vector_tokens = vector_tokens

    def init_pca(self,):
        num_feature_dimensions = 200  # default
        self.pca = PCA(n_components=num_feature_dimensions)
        self.pca.fit(self.vector_features)
        self.neighbors = NearestNeighbors(
            n_neighbors=20, algorithm="brute", metric="euclidean"
        ).fit(self.vector_features)

    def extract(self, img=None):
        """
        Extract a deep feature from an input image

        Parameters
        ----------
        img: Image
            from PIL.Image.open(path) or tensorflow.keras.preprocessing.image.load_img(path)

        Returns
        -------
        feature: Numpy array(s) of predictions.
            (np.ndarray) deep feature with the shape=(2048, )
        """
        img = img.resize((224, 224))  # VGG must take a 224x224 img as an input
        img = img.convert("RGB")  # Make sure img is color
        img_array = image.img_to_array(img)
        expanded_img_array = np.expand_dims(img_array, axis=0)
        preprocessed_img = preprocess_input(expanded_img_array)

        features = self.model.predict(preprocessed_img)
        flattened_features = features.flatten()
        normalized_features = flattened_features / norm(flattened_features)

        return normalized_features

    def search(self, img=None):
        """
        Search a pca features image in the pca features image vector.
        Args:
            img: from PIL.Image.open(path) or tensorflow.keras.preprocessing.image.load_img(path)
        Returns:
            feature (np.ndarray): deep feature with the shape=(4096, )
        """
        input_extract_features = []
        input_extract_features.append(self.extract(img))
        input_features_compressed = self.pca.transform(input_extract_features)

        distances, indices = self.neighbors.kneighbors(input_features_compressed)
        similar_tokens = [self.vectors_tokens[indices[i]] for i in range(0, 20)]
        return similar_tokens

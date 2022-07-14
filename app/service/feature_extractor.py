from pkg_resources import ExtractionError
from tensorflow.keras.preprocessing import image
from numpy.linalg import norm
import numpy as np

from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors

from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input


class FeatureExtractor:
    def __init__(
        self,
        vector_features_full=None,
        # vector_features_pca=None,
        vector_tokens=None,
        num_of_return=10,
    ):
        self.model = ResNet50(
            weights="imagenet",
            include_top=False,
            input_shape=(224, 224, 3),
            pooling="max",
        )

        self.vector_features_full = vector_features_full
        # self.vector_features_pca = vector_features_pca
        self.vector_tokens = vector_tokens
        if vector_features_full == None:
            return
        num_feature_dimensions = 200  # default

        self.pca = PCA(n_components=num_feature_dimensions)
        self.pca.fit(self.vector_features_full)
        self.vector_features_pca = self.pca.transform(self.vector_features_full)
        self.num_of_return = num_of_return

        self.neighbors = NearestNeighbors(
            n_neighbors=self.num_of_return, algorithm="brute", metric="euclidean"
        ).fit(self.vector_features_pca)

    def extract(self, img=None, img_path=None):
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

    def search(self, img=None, img_path=None):
        """
        Search a pca features image in the pca features image vector.

        Parameters
        ----------
        img: Image
            from PIL.Image.open(path) or tensorflow.keras.preprocessing.image.load_img(path)

        Returns
        -------
        list_token_id: array
            returns a list of tokens and ids of the similar images.
        """
        input_extract_features = []
        # extract features from image into 2048-dimension vector
        input_extract_features.append(self.extract(img=img, img_path=img_path))
        # transform the extract features down to 200pc
        input_features_compressed = self.pca.transform(input_extract_features)

        distances, indices = self.neighbors.kneighbors(input_features_compressed)
        print(indices)
        similar_tokens = [
            self.vector_tokens[indices[0][i]] for i in range(0, self.num_of_return)
        ]
        return similar_tokens

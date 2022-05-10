from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors
from tensorflow.keras.preprocessing import image
from feature_extractor import extract_features

from load_vector import vectors_features_pca, vectors_tokens

num_feature_dimensions = 200  # default
pca = PCA(n_components=num_feature_dimensions)
pca.fit(vectors_features_pca)
neighbors = NearestNeighbors(n_neighbors=20, algorithm="brute", metric="euclidean").fit(
    vectors_features_pca
)


def search(img_path=None):
    assert img_path != None, "Image Path must not null"

    input_extract_features = []
    input_extract_features.append(extract_features(img_path))
    input_features_compressed = pca.transform(input_extract_features)

    distances, indices = neighbors.kneighbors(input_features_compressed)
    similar_image_paths = [vectors_tokens[indices[0][i]] for i in range(0, 20)]


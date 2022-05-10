from pkg_resources import ExtractionError
from tensorflow.keras.preprocessing import image
from numpy.linalg import norm
import numpy as np

# from tensorflow.keras.applications.vgg16 import VGG16
# from tensorflow.keras.applications.efficientnet import EfficientNetB4
# from tensorflow.keras.applications.vgg16 import (
#     preprocess_input as vgg16_preprocess_input,
# )

# from tensorflow.keras.applications.resnet50 import (
#     preprocess_input as effnetb4_preprocess_input,
# )

from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input as preprocess_input


model = ResNet50(
    weights="imagenet", include_top=False, input_shape=(224, 224, 3), pooling="max"
)


def extract_features(self, img_path=None):
    """
    Extract a deep features vector from an input image

    Parametors
    ----------
    img_path : str
        The path to the image

    Returns
    -------
    features of an images (np.ndarray): deep feature with the shape=(4096, )
    """
    input_shape = (224, 224, 3)
    img = image.load_img(img_path, target_size=(input_shape[0], input_shape[1]))
    img_array = image.img_to_array(img)
    expanded_img_array = np.expand_dims(img_array, axis=0)
    preprocessed_img = preprocess_input(expanded_img_array)

    features = model.predict(preprocessed_img)
    flattened_features = features.flatten()
    normalized_features = flattened_features / norm(flattened_features)

    return normalized_features

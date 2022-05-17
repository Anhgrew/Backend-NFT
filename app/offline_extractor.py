# Module use to extract feature of whole image database
from PIL import Image
from tqdm import tqdm, tqdm_notebook
from service import FeatureExtractor
from pathlib import Path
import numpy as np
import time

if __name__ == '__main__':
    start = time.time()
    fe = FeatureExtractor()

    for img_path in sorted(Path("./static/Data").glob("*.png")):
        # print(img_path)  # e.g., ./static/img/xxx.jpg
        feature = fe.extract(img=Image.open(img_path))
        # e.g., ./static/feature/xxx.npy
        feature_path = Path("./static/feature") / (img_path.stem + ".npy")
        np.save(feature_path, feature)

    end = time.time()
    print(f"Runtime of the program is {end - start}")

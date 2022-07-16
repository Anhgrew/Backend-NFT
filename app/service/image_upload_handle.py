import io
from PIL import Image
from datetime import datetime

# Handle uploaded image and save to local folder
def handle_uploaded_image(contents, file):
    image = Image.open(io.BytesIO(contents))
    image.load()

    # replace alpha channel with white color
    image = Image.new('RGB', image.size, (255, 255, 255))
    image.paste(image, None)
    uploaded_img_path = (
        "static/uploaded/"
        + datetime.now().isoformat().replace(":", ".")
        + "_"
        + file.filename
    )
    image.save(uploaded_img_path)
    return image, uploaded_img_path

from PIL import Image
from .utils import img_output_name

def resize_image(image_path, width=100, height=100, image_output_name = None):

    try:
        format=image_path.split('.')[-1]

        image_output_name = img_output_name(image_path, format,image_output_name)
        with Image.open(image_path) as img:
            img = img.resize((width, height))
            img.save(image_output_name)
    except Exception as e:
        print(f"An error occurred in resize_image: {e}")
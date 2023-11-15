from PIL import Image
from utils import img_output_name

# def to_jpg(img):
#     return img.convert('RGB')

def to_jpg(img):
    if img.mode == 'RGBA':
        img.load()
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
        img = background
    else:
        img = img.convert('RGB')
    return img



def to_png(img):
    return img

def to_ico(img):
    return img


CONVERSIONS = {
    ('png'  ,  'jpg')    : to_jpg,  
    ('png'  , 'jpeg')    : to_jpg,
    ('png'  ,  'ico')    : to_ico,

    ('jpg'  ,  'png')    : to_png,
    ('jpg'  ,  'ico')    : to_ico,
    ('jpg'  , 'jpeg')    : to_jpg,

    ('ico'  ,  'png')    : to_png,
    ('ico'  ,  'jpg')    : to_jpg,
    ('ico'  , 'jpeg')    : to_jpg,
    
    ('jpeg'  , 'ico')    : to_jpg,
    ('jpeg'  , 'png')    : to_jpg,
    ('jpeg'  , 'jpg')    : to_jpg,
 }



def convert_image(image_path, image_output_name, conversion_func):
    try:
        img = Image.open(image_path)
        converted_img = conversion_func(img)
        converted_img.save(image_output_name)
    except Exception as e:
        print(f"An error occurred in convert_image: {e}")



def convert_format(image_path, format, image_output_name=None):
    try:
        image_output_name = img_output_name(image_path, format,image_output_name)
        ext = image_path.split('.')[-1]
        new_ext = format

        if (ext, new_ext) in CONVERSIONS:
            convert_image(image_path, image_output_name, CONVERSIONS[(ext, new_ext)])
        else:
            print(f"Conversion from {ext} to {new_ext} is not supported.")
    except Exception as e:
        print(f"An error occurred in convert_format: {e}")
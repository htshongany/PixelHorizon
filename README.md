# PixelHorizon

<img src='PixelHorizon.png' alt='PixelHorizon logo'>

PixelHorizon is a command-line tool for image conversion and manipulation. It supports `PNG`, `JPG`, and `ICO` image formats, and provides features to convert between these formats, resize images, and remove image backgrounds. PixelHorizon utilizes the remove.bg API for background removal.

## Installation

To use PixelHorizon, you can clone this repository and install the necessary dependencies with pip:

```
pip install -r requirements.txt
python main.py -h 
```

## API Configuration

To use PixelHorizon's background removal feature, you need to provide your own API key for remove.bg. You can do this by following these steps:

1. Open the `example.env` file in a text editor.
2. Replace `your api key` with your remove.bg API key.
3. Save the file as `.env`.

## Usage

Here's how you can use PixelHorizon to convert an image to another format:

```
python main.py logo.png -f jpg
```

This will convert `logo.png` to `logo.jpg`.

You can also resize an image:

```
python main.py logo.png --width 100 --height 100
```

This will resize `logo.png` to a width and height of 100. Please note that resizing is designed to reduce the size of images. Enlarging an image may result in quality loss as PixelHorizon does not support upscaling.

To remove an image's background:

```
python main.py logo.png -r 
```

This will remove the background of `logo.png` using the remove.bg API. Here’s an example of how it works:

<img src='tests/logo.jpeg' alt='Before background removal' width=200> 
<img src='tests/logo.png' alt='After background removal' width=200>

In the above images, the first image is the original image and the second image is the result after running the --remove-bg command. As you can see, the background has been successfully removed.

Please note that the effectiveness of background removal can vary depending on the complexity of the image. For best results, use images with clear contrast between the subject and the background.
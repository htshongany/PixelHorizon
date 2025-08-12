from PIL import Image
import os
from .utils import get_image_name

# --- Internal Helper Functions ---

def _to_jpg(img: Image.Image) -> Image.Image:
    """Converts a PIL Image to JPG format, handling transparency by adding a white background."""
    if img.mode == 'RGBA':
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
        return background
    return img.convert('RGB')

def _to_png(img: Image.Image) -> Image.Image:
    """Ensures the image is in a mode compatible with PNG (no-op for most common cases)."""
    return img

def _to_ico(img: Image.Image) -> Image.Image:
    """Ensures the image is in a mode compatible with ICO (no-op for most common cases)."""
    return img

# --- Public API ---

CONVERSIONS = {
    'jpg': _to_jpg,
    'jpeg': _to_jpg,
    'png': _to_png,
    'ico': _to_ico,
}

def convert_format(image_path: str, output_format: str, custom_output_path: str = None) -> str:
    """
    Converts an image file to a different format (e.g., PNG to JPG).

    If no custom output path is provided, a new path is generated in the same
    directory with the new format as the extension (e.g., 'logo.png' -> 'logo.jpg').

    Args:
        image_path (str): Path to the source image file.
        output_format (str): The target format (e.g., 'jpg', 'png', 'ico').
        custom_output_path (str, optional): The exact path to save the new file to.
                                            Defaults to None.

    Returns:
        str: The path where the converted image was saved.

    Raises:
        ValueError: If the requested output format is not supported.
        FileNotFoundError: If the source image_path does not exist.
        IOError: If there is an error reading the source or writing the output file.
    """
    output_format = output_format.lower()
    if output_format not in CONVERSIONS:
        raise ValueError(f"Conversion to format '{output_format}' is not supported.")

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"The file '{image_path}' was not found.")

    try:
        with Image.open(image_path) as img:
            # Determine the output path
            if custom_output_path:
                output_path = custom_output_path
            else:
                base_name = get_image_name(image_path)
                source_dir = os.path.dirname(image_path)
                output_path = os.path.join(source_dir, f"{base_name}.{output_format}")

            # Get the correct conversion function and apply it
            conversion_func = CONVERSIONS[output_format]
            converted_img = conversion_func(img)

            # Save the final image
            converted_img.save(output_path)
            
            return output_path

    except Exception as e:
        raise IOError(f"An error occurred during image conversion: {e}")

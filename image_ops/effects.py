from PIL import Image
import os
from .utils import get_image_name, get_extension

def apply_grayscale(image_path: str, custom_output_path: str = None) -> str:
    """
    Applies a grayscale filter to an image.

    If no custom output path is provided, a new path is generated in the same
    directory with a '_grayscale' suffix (e.g., 'logo.png' -> 'logo_grayscale.png').

    Args:
        image_path (str): Path to the source image file.
        custom_output_path (str, optional): The exact path to save the new file to.
                                            Defaults to None.

    Returns:
        str: The path where the grayscale image was saved.

    Raises:
        FileNotFoundError: If the source image_path does not exist.
        IOError: If there is an error reading the source or writing the output file.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"The file '{image_path}' was not found.")

    try:
        with Image.open(image_path) as img:
            # Determine the output path
            if custom_output_path:
                output_path = custom_output_path
            else:
                base_name = get_image_name(image_path)
                ext = get_extension(image_path)
                source_dir = os.path.dirname(image_path)
                output_path = os.path.join(source_dir, f"{base_name}_grayscale.{ext}")

            # Convert to grayscale ('L' mode) and save
            grayscale_img = img.convert('L')
            grayscale_img.save(output_path)
            
            return output_path
            
    except Exception as e:
        raise IOError(f"An error occurred during grayscale conversion: {e}")

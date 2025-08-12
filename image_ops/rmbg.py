import requests
import os
from .utils import get_image_name

def remove_background(image_path: str, api_key: str, custom_output_path: str = None) -> str:
    """
    Removes the background from an image using the remove.bg API.

    If no custom output path is provided, a new path is generated in the same
    directory with a '_no-bg.png' suffix (e.g., 'logo.jpg' -> 'logo_no-bg.png').
    The output is always a PNG to support transparency.

    Args:
        image_path (str): Path to the source image file.
        api_key (str): Your API key for the remove.bg service.
        custom_output_path (str, optional): The exact path to save the new file to.
                                            Defaults to None.

    Returns:
        str: The path where the processed image was saved.

    Raises:
        ValueError: If the API key is missing or if the API returns an error.
        FileNotFoundError: If the source image_path does not exist.
        IOError: If there is a network error or an issue writing the output file.
    """
    if not api_key:
        raise ValueError("Remove.bg API key is missing. Please provide it via the API_KEY environment variable.")
    
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"The file '{image_path}' was not found.")

    # Determine the output path
    if custom_output_path:
        output_path = custom_output_path
    else:
        base_name = get_image_name(image_path)
        source_dir = os.path.dirname(image_path)
        # Output is always PNG for transparency
        output_path = os.path.join(source_dir, f"{base_name}_no-bg.png")

    try:
        with open(image_path, 'rb') as image_file:
            response = requests.post(
                'https://api.remove.bg/v1.0/removebg',
                files={'image_file': image_file},
                data={'size': 'auto'},
                headers={'X-Api-Key': api_key},
                timeout=30  # 30-second timeout for the request
            )
        
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)

        with open(output_path, 'wb') as out_file:
            out_file.write(response.content)
        
        return output_path
            
    except requests.exceptions.RequestException as e:
        raise IOError(f"A network error occurred: {e}")
    except Exception as e:
        raise IOError(f"An unexpected error occurred while processing the background removal: {e}")

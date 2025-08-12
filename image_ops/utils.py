import os

def get_image_name(image_path: str) -> str:
    """
    Extracts the base name of a file from its path, without the extension.

    Example:
        get_image_name("C:/Users/Test/logo.png") -> "logo"

    Args:
        image_path (str): The full or relative path to the image.

    Returns:
        str: The base name of the file.
    """
    return os.path.splitext(os.path.basename(image_path))[0]

def get_extension(image_path: str) -> str:
    """
    Extracts the extension of a file from its path, without the dot.

    Example:
        get_extension("C:/Users/Test/logo.png") -> "png"

    Args:
        image_path (str): The full or relative path to the image.

    Returns:
        str: The file extension.
    """
    return os.path.splitext(image_path)[1][1:].lower()

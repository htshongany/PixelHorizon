import os
import subprocess
from PIL import Image

def vectorize_image(
    input_path: str, 
    custom_output_path: str = None, 
    turd_size: int = 2, 
    color: str = '#000000'
) -> str:
    """
    Converts a raster image (PNG, JPG, etc.) into an SVG vector file using Potrace.

    This function requires 'potrace.exe' to be available in the system's PATH
    or in the project's root directory.

    Args:
        input_path (str): Path to the source raster image.
        custom_output_path (str, optional): The exact path to save the SVG file.
                                            If None, a path is generated automatically.
        turd_size (int, optional): Parameter to control noise removal. Defaults to 2.
        color (str, optional): Hex code for the vector color. Defaults to '#000000'.

    Returns:
        str: The path where the converted SVG image was saved.

    Raises:
        FileNotFoundError: If the input file or 'potrace.exe' cannot be found.
        ValueError: If the color format is invalid.
        IOError: If Potrace fails or if there's an issue with file operations.
    """
    potrace_executable = "potrace.exe"
    
    # Check for potrace.exe in the project's bin directory first
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    local_potrace_path = os.path.join(project_root, "bin", potrace_executable)

    if os.path.exists(local_potrace_path):
        potrace_executable = local_potrace_path
    # If not found locally, check the system's PATH
    elif not any(os.access(os.path.join(path, potrace_executable), os.X_OK) for path in os.environ["PATH"].split(os.pathsep)):
        raise FileNotFoundError(f"'{potrace_executable}' not found in the project's 'bin' directory or in the system's PATH. Please install Potrace.")

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"The input file '{input_path}' was not found.")

    # Determine output path
    if custom_output_path:
        output_path = custom_output_path
    else:
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        source_dir = os.path.dirname(input_path)
        output_path = os.path.join(source_dir, f"{base_name}.svg")

    # Create a temporary BMP file for Potrace
    temp_bmp_path = output_path + ".temp.bmp"

    try:
        # Convert source image to a 1-bit BMP file
        with Image.open(input_path) as img:
            img.convert('1').save(temp_bmp_path)

        # Build and run the Potrace command
        command = [
            potrace_executable,
            temp_bmp_path,
            "--svg",
            "-o", output_path,
            "--turdsize", str(turd_size),
            "--color", color
        ]
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        
        return output_path

    except subprocess.CalledProcessError as e:
        error_message = e.stderr.strip()
        raise IOError(f"Potrace failed with error: {error_message}")
    except Exception as e:
        raise IOError(f"An unexpected error occurred during vectorization: {e}")
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_bmp_path):
            os.remove(temp_bmp_path)

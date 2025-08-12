import argparse
import os
from image_ops.convert import convert_format
from image_ops.rmbg import remove_background
from image_ops.resize import resize_image
from dotenv import load_dotenv


load_dotenv()
import argparse
import os
import sys
from dotenv import load_dotenv

# Add the project root to the Python path to allow absolute imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from image_ops import convert, resize, rmbg

# Load environment variables from a .env file
load_dotenv()
REMOVE_BG_API_KEY = os.getenv("REMOVE_BG_API_KEY")

def main():
    """Main function to parse arguments and call image operations."""
    parser = argparse.ArgumentParser(
        description="PixelHorizon: A command-line tool for image manipulation.",
        epilog="Example: python main.py logo.png --format jpg --resize 100 100"
    )
    parser.add_argument('image_paths', type=str, nargs='+', help='One or more paths to the image files.')
    
    # --- Operations ---
    parser.add_argument('--format', type=str, help='Convert image to a new format.', choices=['jpg', 'jpeg', 'png', 'ico'])
    parser.add_argument('--resize', type=int, nargs=2, metavar=('WIDTH', 'HEIGHT'), help='Resize image to a specific width and height.')
    parser.add_argument('--remove-bg', action='store_true', help='Remove the image background (requires REMOVE_BG_API_KEY).')

    # --- Options ---
    parser.add_argument('-o', '--output', type=str, help='Specify a custom output file path. If not provided, a name will be generated automatically.')

    args = parser.parse_args()

    for image_path in args.image_paths:
        if not os.path.exists(image_path):
            print(f"Error: The file '{image_path}' does not exist. Skipping.")
            continue

        print(f"Processing '{os.path.basename(image_path)}'...")
        
        try:
            current_path = image_path
            
            if args.resize:
                width, height = args.resize
                print(f"  - Resizing to {width}x{height}...")
                current_path = resize.resize_image(current_path, width, height, custom_output_path=args.output)
                print(f"    -> Resized image saved to: {current_path}")

            if args.remove_bg:
                print("  - Removing background...")
                if not REMOVE_BG_API_KEY:
                    print("    -> Error: REMOVE_BG_API_KEY is not set. Skipping background removal.")
                else:
                    current_path = rmbg.remove_background(current_path, REMOVE_BG_API_KEY, custom_output_path=args.output)
                    print(f"    -> Background removed. Image saved to: {current_path}")

            if args.format:
                print(f"  - Converting to {args.format}...")
                current_path = convert.convert_format(current_path, args.format, custom_output_path=args.output)
                print(f"    -> Converted image saved to: {current_path}")

        except (ValueError, FileNotFoundError, IOError) as e:
            print(f"  -> An error occurred: {e}")
        
        print("-" * 20)

if __name__ == '__main__':
    main()


def main():
    parser = argparse.ArgumentParser(description='Process some images.')
    parser.add_argument('image_paths', type=str, nargs='+', help='path to the image files')
    parser.add_argument('--width', type=int, help='width of the image')
    parser.add_argument('--height', type=int, help='height of the image')
    parser.add_argument('-r','--remove-bg', action='store_true', help='remove the background of the image')
    parser.add_argument('-f','--format', type=str, help='output format of the image', choices=['jpg','jpeg', 'png', 'ico'])
    parser.add_argument('-o','--output', type=str, help='output name')
    args = parser.parse_args()

    for image_path in args.image_paths:
        try:
            if args.width and args.height:
                resize_image(image_path, args.width, args.height,image_output_name=args.output )

            if args.remove_bg:
                remove_background(image_path, api_key = remove_bg_api_key, image_output_name=args.output)

            if args.format:
                convert_format(image_path, args.format, image_output_name=args.output)
        except Exception as e:
            print(f"An error occurred in main: {e}")

if __name__ == '__main__':
    main()
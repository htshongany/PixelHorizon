import argparse
import os
from image_ops.convert import convert_format
from image_ops.rmbg import remove_background
from image_ops.resize import resize_image
from dotenv import load_dotenv


load_dotenv()
remove_bg_api_key = os.getenv("API_KEY")

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
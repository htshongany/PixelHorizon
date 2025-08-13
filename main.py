import argparse
import os
import sys
import glob
import tempfile
import shutil
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from image_ops import convert, resize, rmbg, effects, vectorize

# Load environment variables
load_dotenv()
REMOVE_BG_API_KEY = os.getenv("REMOVE_BG_API_KEY")

def main():
    """Main function to parse arguments and call image operations."""
    console = Console()
    parser = argparse.ArgumentParser(
        description="[bold cyan]PixelHorizon[/bold cyan]: A modern command-line tool for image manipulation.",
        epilog="Example: python main.py -i ./images -p '*.png' -g -o ./processed",
        formatter_class=argparse.RawTextHelpFormatter
    )

    # --- Input Arguments ---
    input_group = parser.add_argument_group('Input Options')
    input_group.add_argument('image_paths', type=str, nargs='*', help='(Optional) One or more direct paths to image files.')
    input_group.add_argument('-i', '--input-dir', type=str, help='Directory to search for images.')
    input_group.add_argument('-p', '--pattern', type=str, help='Pattern to match files (e.g., "*.png"). If not provided, matches all supported types.')

    # --- Operations ---
    op_group = parser.add_argument_group('Image Operations')
    op_group.add_argument('-f', '--format', type=str, help='Convert image to a new format.', choices=['jpg', 'jpeg', 'png', 'ico'])
    op_group.add_argument('-rs', '--resize', type=int, nargs=2, metavar=('W', 'H'), help='Resize image.')
    op_group.add_argument('-rb', '--remove-bg', action='store_true', help='Remove background.')
    op_group.add_argument('-g', '--grayscale', action='store_true', help='Apply grayscale filter.')
    op_group.add_argument('--to-svg', action='store_true', help='Convert image to SVG.')

    # --- SVG Options ---
    svg_group = parser.add_argument_group('SVG Conversion Options')
    svg_group.add_argument('--svg-color', type=str, default='#000000', metavar='HEX', help="SVG vector color (default: #000000).")
    svg_group.add_argument('--svg-turd-size', type=int, default=2, metavar='N', help="Noise removal size for SVG (default: 2).")

    # --- Output Options ---
    out_group = parser.add_argument_group('Output Options')
    out_group.add_argument('-o', '--output', type=str, help='Specify an output file path or directory.')

    args = parser.parse_args()

    # --- File Discovery ---
    files_to_process = list(args.image_paths)
    if args.input_dir:
        if os.path.isfile(args.input_dir):
            files_to_process.append(args.input_dir)
        elif os.path.isdir(args.input_dir):
            if args.pattern:
                search_path = os.path.join(args.input_dir, args.pattern)
                files_to_process.extend(glob.glob(search_path))
            else:
                # Default patterns if none provided
                default_patterns = ['*.png', '*.jpg', '*.jpeg', '*.ico']
                for pattern in default_patterns:
                    search_path = os.path.join(args.input_dir, pattern)
                    files_to_process.extend(glob.glob(search_path))
        else:
            console.print(f"[red]Error: Input path '{args.input_dir}' not found.[/red]")
            return

    if not files_to_process:
        console.print("[yellow]No image files found to process.[/yellow]")
        return

    # --- Output Handling ---
    output_dir = None
    output_file_path = None
    if args.output:
        if os.path.isdir(args.output) or ('.' not in os.path.basename(args.output) and len(files_to_process) > 1):
             output_dir = args.output
             if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                console.print(f"Created output directory: [cyan]{output_dir}[/cyan]")
        elif len(files_to_process) == 1:
            output_file_path = args.output
        else:
            console.print("[red]Error: Custom file output (-o) can only be used with a single input image.[/red]")
            return

    # --- Processing Loop ---
    with Progress(console=console) as progress:
        task = progress.add_task("[cyan]Processing...", total=len(files_to_process))

        for image_path in files_to_process:
            progress.update(task, advance=1, description=f"Processing [bold]{os.path.basename(image_path)}[/bold]")
            
            with tempfile.TemporaryDirectory() as temp_dir:
                try:
                    current_path = image_path
                    
                    # --- Operation Chaining ---
                    if args.resize:
                        width, height = args.resize
                        temp_output = os.path.join(temp_dir, os.path.basename(current_path))
                        current_path = resize.resize_image(current_path, width, height, custom_output_path=temp_output)
                    
                    if args.grayscale:
                        temp_output = os.path.join(temp_dir, os.path.basename(current_path))
                        current_path = effects.apply_grayscale(current_path, custom_output_path=temp_output)

                    if args.remove_bg:
                        if not REMOVE_BG_API_KEY:
                            console.print("[yellow]Warning: REMOVE_BG_API_KEY not set. Skipping background removal.[/yellow]")
                        else:
                            temp_output = os.path.join(temp_dir, os.path.splitext(os.path.basename(current_path))[0] + ".png")
                            current_path = rmbg.remove_background(current_path, REMOVE_BG_API_KEY, custom_output_path=temp_output)
                    
                    # --- Final Conversion/Output ---
                    final_ext = args.format if args.format else os.path.splitext(current_path)[1][1:]
                    if args.to_svg:
                        final_ext = 'svg'

                    # Determine final output path
                    if output_file_path:
                        final_path = output_file_path
                    elif output_dir:
                        base_name = os.path.splitext(os.path.basename(image_path))[0]
                        final_path = os.path.join(output_dir, f"{base_name}.{final_ext}")
                    else: # Default: save alongside original
                        base_name = os.path.splitext(os.path.basename(image_path))[0]
                        source_dir = os.path.dirname(image_path)
                        final_path = os.path.join(source_dir, f"{base_name}_processed.{final_ext}")

                    # Execute final operation (SVG or format conversion)
                    if args.to_svg:
                        vectorize.vectorize_image(current_path, custom_output_path=final_path, turd_size=args.svg_turd_size, color=args.svg_color)
                    elif args.format:
                        convert.convert_format(current_path, args.format, custom_output_path=final_path)
                    else:
                        # If no final conversion, just move the last processed file
                        shutil.copy(current_path, final_path)

                except (ValueError, FileNotFoundError, IOError) as e:
                    console.print(f"\n[red]Error processing {os.path.basename(image_path)}: {e}[/red]")

    console.print("[bold green]All tasks complete![/bold green]")

if __name__ == '__main__':
    main()
# PixelHorizon

<p align="center">
  <img src="assets/PixelHorizon.png" alt="PixelHorizon logo" width="200"/>
</p>

<p align="center">
  <strong>A modern, feature-rich command-line tool for powerful image manipulation.</strong>
</p>

---

### Why PixelHorizon?

PixelHorizon is designed for developers, designers, and anyone who needs to perform image operations quickly and efficiently without leaving the terminal. It excels at **batch processing**—applying one or more actions to a whole folder of images at once—and provides a clean, user-friendly experience from start to finish.

### ✨ Features

-   🗂️ **Flexible Input**: Process a single image, a list of images, or an entire directory.
-   🔎 **Pattern Matching**: Filter files in a directory with patterns like `*.png` or `logo-*.jpg`.
-   ⛓️ **Operation Chaining**: Combine multiple actions (e.g., remove background, then resize) in one command.
-   📤 **Clean Output**: Send all processed files to a dedicated output directory, keeping your source folder untouched.
-   🔄 **Format Conversion**: Convert between `PNG`, `JPG`, and `ICO`.
-   📐 **Resizing**: Easily resize images to specific dimensions. Note that this is best used for reducing image size; enlarging images may result in quality loss.
-   🎨 **Effects**: Apply a grayscale filter or vectorize line art into a clean `SVG`.
-   ✂️ **Background Removal**: Automatically remove backgrounds using the [remove.bg](https://www.remove.bg/) API.
-   📊 **Rich Feedback**: A clean progress bar shows you the status of your batch operations.

---

### 🚀 Getting Started

#### 1. Installation

First, clone the repository and install the required Python packages.

```bash
git clone https://github.com/your-username/PixelHorizon.git
cd PixelHorizon
pip install -r requirement.txt
```

#### 2. Configuration

-   **For Background Removal**: This feature requires an API key from [remove.bg](https://www.remove.bg/fr/dashboard#api-key).
    1.  Rename `exemple.env` to `.env`.
    2.  Open the `.env` file and add your key: `REMOVE_BG_API_KEY="your_key_here"`

-   **For SVG Vectorization**: This feature uses Potrace. For Windows, download the `potrace.exe` binary from the [official website](https://potrace.sourceforge.net/) and place it inside a `bin` folder at the project's root. For other systems, ensure Potrace is installed and available in your system's PATH.

---

### 📚 How to Use

PixelHorizon is built to be intuitive. Here are some common use cases.

#### Use Case 1: Batch Processing a Directory

This is PixelHorizon's superpower. Let's convert all JPG and PNG images in a folder named `source_images` to grayscale and save them in a new folder called `processed`.

```bash
python main.py -i ./source_images -g -o ./processed
```

The script automatically finds all supported images, applies the filter, and the progress bar keeps you updated.

#### Use Case 2: Background Removal

To remove the background from an image, use the `-rb` flag.

```bash
python main.py my_image.png -rb -o ./outputs
```

The result is a clean PNG with a transparent background.

<table align="center" style="margin: 20px auto;">
  <tr>
    <td align="center"><strong>Before</strong></td>
    <td align="center"><strong>After</strong></td>
  </tr>
  <tr>
    <td><img src="assets/logo.jpeg" alt="Before background removal" width="250"></td>
    <td><img src="assets/logo.png" alt="After background removal" width="250"></td>
  </tr>
</table>

#### Use Case 3: Vectorizing an Image

Convert a raster image (like PNG) into a clean, scalable SVG vector graphic.

```bash
python main.py assets/simple-logo.png --to-svg
```

<table align="center" style="margin: 20px auto;">
  <tr>
    <td align="center"><strong>Before (PNG)</strong></td>
    <td align="center"><strong>After (SVG)</strong></td>
  </tr>
  <tr>
    <td><img src="assets/simple-logo.png" alt="Before vectorization" width="250"></td>
    <td><img src="assets/simple-logo.svg" alt="After vectorization" width="250"></td>
  </tr>
</table>

#### Use Case 4: Chaining Multiple Operations

You can combine actions. For example, let's take an image, remove its background, resize it to 256x256 pixels, and convert it to the JPG format.

```bash
python main.py avatar.png -rb -rs 256 256 -f jpg -o ./final_avatar.jpg
```

---

### 🔮 Future Features

We're always looking to improve PixelHorizon. Here are some features planned for future releases:

-   **AI Image Upscaling**: Integration with AI models to allow for high-quality image enlargement.
-   **Graphical User Interface (UI)**: A simple, intuitive UI for users who prefer a visual workflow over the command line.

### 💻 Full Command List

For a complete list of all commands and their aliases, run the help command:

```bash
python main.py -h
```

### 🧪 Development

This project uses `unittest` for testing. To run the full test suite:

```bash
python -m unittest discover tests
```

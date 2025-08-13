import sys
import os
import unittest
from PIL import Image

# Adjust the path to import from the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from image_ops.resize import resize_image
from image_ops.utils import get_image_name

class TestImageResize(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.input_image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'logo.png'))
        self.output_dir = os.path.dirname(__file__)
        self.test_image_name = get_image_name(self.input_image_path)
        self.output_files = []

    def tearDown(self):
        """Clean up after each test."""
        for file_path in self.output_files:
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_resize_image(self):
        """Test resizing an image to a specific dimension."""
        width, height = 100, 150
        output_path = os.path.join(self.output_dir, f"{self.test_image_name}_resized.png")
        self.output_files.append(output_path)

        result_path = resize_image(self.input_image_path, width, height, custom_output_path=output_path)

        self.assertTrue(os.path.exists(result_path))
        with Image.open(result_path) as img:
            self.assertEqual(img.size, (width, height))
        self.assertEqual(result_path, output_path)

if __name__ == '__main__':
    unittest.main(verbosity=2)


import sys
import os
import unittest
from PIL import Image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from image_ops.convert import convert_format
from image_ops.utils import get_image_name

class TestImageConversion(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.input_image_path = os.path.join(os.path.dirname(__file__), 'logo.png')
        self.output_dir = os.path.dirname(__file__)
        self.test_image_name = get_image_name(self.input_image_path)
        self.output_files = []

    def tearDown(self):
        """Clean up after each test."""
        for file_path in self.output_files:
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_convert_format_to_jpg(self):
        """Test converting a file to JPG format."""
        output_format = 'jpg'
        output_path = os.path.join(self.output_dir, f"{self.test_image_name}_converted.{output_format}")
        self.output_files.append(output_path)

        result_path = convert_format(self.input_image_path, output_format, custom_output_path=output_path)
        
        self.assertTrue(os.path.exists(result_path))
        with Image.open(result_path) as img:
            self.assertEqual(img.format, 'JPEG')
        self.assertEqual(result_path, output_path)

    def test_convert_format_to_ico(self):
        """Test converting a file to ICO format."""
        output_format = 'ico'
        output_path = os.path.join(self.output_dir, f"{self.test_image_name}_converted.{output_format}")
        self.output_files.append(output_path)

        result_path = convert_format(self.input_image_path, output_format, custom_output_path=output_path)
        
        self.assertTrue(os.path.exists(result_path))
        with Image.open(result_path) as img:
            self.assertIn(img.format, ['ICO', 'PNG'])
        self.assertEqual(result_path, output_path)

    def test_convert_format_no_output_path(self):
        """Test conversion when no output path is specified."""
        output_format = 'jpg'
        expected_path = os.path.join(self.output_dir, f"{self.test_image_name}.{output_format}")
        self.output_files.append(expected_path)

        result_path = convert_format(self.input_image_path, output_format)
        self.assertTrue(os.path.exists(result_path))
        self.assertEqual(result_path, expected_path)


if __name__ == '__main__':
    unittest.main(verbosity=2)

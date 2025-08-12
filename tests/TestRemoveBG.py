import sys
import os
import unittest
from dotenv import load_dotenv
from PIL import Image

# Adjust the path to import from the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from image_ops.rmbg import remove_background
from image_ops.utils import get_image_name

# Load environment variables from .env file
load_dotenv()
REMOVE_BG_API_KEY = os.getenv("REMOVE_BG_API_KEY")

@unittest.skipIf(not REMOVE_BG_API_KEY, "Skipping remove.bg tests because API_KEY is not set.")
class TestRemoveBG(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.input_image_path = os.path.join(os.path.dirname(__file__), 'logo.jpeg')
        self.output_dir = os.path.dirname(__file__)
        self.test_image_name = get_image_name(self.input_image_path)
        self.output_files = []

    def tearDown(self):
        """Clean up after each test."""
        for file_path in self.output_files:
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_remove_background(self):
        """Test removing the background from an image."""
        output_path = os.path.join(self.output_dir, f"{self.test_image_name}_no_bg.png")
        self.output_files.append(output_path)

        try:
            result_path = remove_background(self.input_image_path, REMOVE_BG_API_KEY, custom_output_path=output_path)
            
            self.assertTrue(os.path.exists(result_path))
            self.assertEqual(result_path, output_path)
            # Verify that the output is a valid image
            with Image.open(result_path) as img:
                self.assertIn(img.format, ['PNG'])

        except ValueError as e:
            # This allows the test to pass gracefully if the API key is invalid
            # or if there's a known API issue, by failing the assertion.
            self.fail(f"API call failed: {e}")
        except IOError as e:
            self.fail(f"File or network error occurred: {e}")


if __name__ == '__main__':
    unittest.main(verbosity=2)


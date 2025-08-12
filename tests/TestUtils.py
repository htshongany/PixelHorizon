import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from image_ops.utils import get_image_name, get_extension

class TestUtils(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.test_path_unix = "/home/user/images/logo.png"
        self.test_path_windows = "C:\\Users\\user\\images\\logo.png"
        self.test_path_simple = "logo.jpeg"

    def test_get_image_name(self):
        """Test extracting the base name of an image file."""
        self.assertEqual(get_image_name(self.test_path_unix), "logo")
        self.assertEqual(get_image_name(self.test_path_windows), "logo")
        self.assertEqual(get_image_name(self.test_path_simple), "logo")

    def test_get_extension(self):
        """Test extracting the file extension."""
        self.assertEqual(get_extension(self.test_path_unix), "png")
        self.assertEqual(get_extension(self.test_path_windows), "png")
        self.assertEqual(get_extension(self.test_path_simple), "jpeg")

if __name__ == '__main__':
    unittest.main(verbosity=2)

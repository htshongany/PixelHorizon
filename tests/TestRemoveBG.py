import sys , os
sys.path.append('..')
import unittest
import requests
from image_ops.rmbg import remove_background
from dotenv import load_dotenv


load_dotenv()
remove_bg_api_key = os.getenv("API_KEY")


class TestRemoveBG(unittest.TestCase):

    def test_remove_background(self):
        self.assertEqual(remove_background('logo.jpeg', remove_bg_api_key), requests.codes.ok)


if __name__ == '__main__':
    unittest.main()

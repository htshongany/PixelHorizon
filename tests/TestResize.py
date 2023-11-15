import sys
sys.path.append('..')

import unittest
from PIL import Image
from image_ops.resize import resize_image

class TestImageResize(unittest.TestCase):
   
    def test_resize_image(self):

        resize_image('logo.jpeg', width=100, height=100,image_output_name="img_resize.jpeg")

        with Image.open('img_resize.jpeg') as img:
            self.assertEqual(img.size, (100, 100))

if __name__ == '__main__':
    unittest.main()

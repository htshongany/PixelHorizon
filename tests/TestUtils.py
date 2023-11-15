import sys , os
sys.path.append('..')
import unittest
import time 
from hashlib import blake2b
from image_ops.utils import hash_string , hash_output_name , img_output_name



def img_output_name(image_path, format,output_name=None):
    
    if output_name == None:
        return hash_output_name(image_path,format)
    else:
        if output_name.split('.')[-1] != format:
            return output_name +'.'+format

        return output_name

class TestU(unittest.TestCase):

    def test_hash_string(self):
        self.assertEqual(blake2b(key=bytes('test', encoding='utf-8'), digest_size=5).hexdigest(), blake2b(key=b'test', digest_size=5).hexdigest())

    def test_hash_output_name(self):
        hash_str = hash_string(str(int(time.time()))) +'.png'
        self.assertEqual(hash_str.split('.')[-1], 'png')

    def test_img_output_name(self):

        output_name_1 = img_output_name('logo.jpeg', 'jpeg',output_name=None)
        output_name_2 = img_output_name('logo.jpeg', 'png', output_name='main')
        output_name_3 = img_output_name('logo.jpeg', 'jpeg',output_name="main.jpeg")
    
        self.assertEqual(output_name_1, hash_string(str(int(time.time()))) +'.jpeg')
        self.assertEqual(output_name_2, 'main.png')
        self.assertEqual(output_name_3, 'main.jpeg')


if __name__ == '__main__':
    unittest.main()

import sys , os
sys.path.append('..')

import unittest
from PIL import Image
from image_ops.convert import convert_format, to_jpg, to_png, to_ico  # Assurez-vous de remplacer 'your_module' par le nom de votre module

class TestImageConversion(unittest.TestCase):
    def test_to_jpg(self):
        # Ouvrir une image réelle
        with Image.open('logo.png') as img:
            # Appeler la fonction avec une image réelle
            converted_img = to_jpg(img)

            # Vérifier que l'image a été convertie en RGB
            self.assertEqual(converted_img.mode, 'RGB')

    # Vous pouvez ajouter des méthodes de test similaires pour to_png et to_ico

    def test_convert_format(self):
        # Appeler la fonction avec un chemin d'image réel
        convert_format('logo.png', 'jpg', 'logo_converted.jpg')

        # Ouvrir l'image convertie et vérifier son format
        with Image.open('logo_converted.jpg') as img:
            self.assertEqual(img.format, 'JPEG')



if __name__ == '__main__':
    unittest.main()

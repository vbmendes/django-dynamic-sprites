from django.test import TestCase

from dynamic_sprites.image import Image

class ImageTestCase(TestCase):
    
    def test_dimensions_for_brazil(self):
        image = Image('country/flags/brazil.gif')
        self.assertEqual(476, image.width)
        self.assertEqual(330, image.height)
    
    def test_dimensions_for_usa(self):
        image = Image('country/flags/usa.jpg')
        self.assertEqual(475, image.width)
        self.assertEqual(335, image.height)

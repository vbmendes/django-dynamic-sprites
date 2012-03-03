import os

from django.conf import settings
from django.test import TestCase

from dynamic_sprites.image import Image, OutputImage

from helpers import get_absolute_path


class ImageTestCase(TestCase):

    def test_dimensions_for_brazil(self):
        image = Image(get_absolute_path('country/flags/brazil.gif'))
        self.assertEqual(476, image.width)
        self.assertEqual(330, image.height)
        self.assertEqual(476, image.maxside)
        self.assertEqual(476 * 330, image.area)

    def test_dimensions_for_usa(self):
        image = Image(get_absolute_path('country/flags/usa.jpg'))
        self.assertEqual(475, image.width)
        self.assertEqual(335, image.height)
        self.assertEqual(475, image.maxside)
        self.assertEqual(475 * 335, image.area)

    def test_image_filename_and_format(self):
        image = Image(get_absolute_path('country/flags/usa.jpg'))
        self.assertEqual('usa', image.filename)
        self.assertEqual('jpg', image.format)


class OutputImageTestCase(TestCase):

    def test_image_can_be_saved(self):
        image1 = Image(get_absolute_path('country/flags/bra.png'))
        image2 = Image(get_absolute_path('country/flags/can.png'))
        image3 = Image(get_absolute_path('country/flags/usa.png'))
        out_image = OutputImage(48 * 3, 48)
        out_image.add(image1, 0, 0)
        out_image.add(image2, 48, 0)
        out_image.add(image3, 96, 0)

        path = 'country/flags/sprite.png'
        absolute_path = os.path.join(settings.MEDIA_ROOT, path)
        try:
            out_image.save(absolute_path)
            self.assertTrue(os.path.exists(absolute_path))
            generated_from_fs = Image(absolute_path)
            self.assertEqual(out_image.width, generated_from_fs.width)
            self.assertEqual(out_image.height, generated_from_fs.height)
        finally:
            os.remove(absolute_path)

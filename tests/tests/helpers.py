# coding: utf8

import os

from django.conf import settings

from dynamic_sprites.image import Image


class MockedImage(object):
    pass


def get_absolute_path(path):
    return os.path.join(settings.MEDIA_ROOT, path)


class SpriteTestCaseMixin(object):

    def test_sprite_image(self):
        generated = self.sprite.generate()
        self.assertEqual(self.sprite.width, generated.width)
        self.assertEqual(self.sprite.height, generated.height)

        path = 'country/flags/sprite.png'
        absolute_path = os.path.join(settings.MEDIA_ROOT, path)

        try:
            generated.save(absolute_path)
            self.assertTrue(os.path.exists(absolute_path))
            generated_from_fs = Image(absolute_path)
            self.assertEqual(generated.width, generated_from_fs.width)
            self.assertEqual(generated.height, generated_from_fs.height)
        finally:
            os.remove(absolute_path)

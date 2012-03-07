# coding: utf8

from django.test import TestCase

from dynamic_sprites.packing import BinPacking, HorizontalPacking, VerticalPacking
from dynamic_sprites.sprite import Sprite

from helpers import get_absolute_path, SpriteTestCaseMixin


class TestEmptySpriteTestCase(TestCase, SpriteTestCaseMixin):

    def setUp(self):
        self.sprite = Sprite('flags', images=[])

    def test_dimensions(self):
        self.assertEqual(1, self.sprite.width)
        self.assertEqual(1, self.sprite.height)


class HorizontalSpriteTestCase(TestCase, SpriteTestCaseMixin):

    def setUp(self):
        self.sprite = Sprite('flags',
            images=[
                ('brazil', get_absolute_path('country/flags/brazil.gif')),
                ('usa', get_absolute_path('country/flags/usa.jpg')),
            ],
            packing_class=HorizontalPacking
        )

    def test_name(self):
        self.assertEqual('flags', self.sprite.name)

    def test_css_class(self):
        self.assertEqual('sprite-flags', self.sprite.css_class)

    def test_dimensions(self):
        self.assertEqual(475 + 476, self.sprite.width)
        self.assertEqual(max(335, 330), self.sprite.height)

    def test_sprite_css(self):
        css = self.sprite.generate_css('image_url.png')
        self.assertTrue(isinstance(css, basestring))
        self.assertTrue('.sprite-flags' in css)
        self.assertTrue('.sprite-flags-brazil{background-position:-0px -0px}' in css)


class VerticalSpriteTestCase(TestCase, SpriteTestCaseMixin):

    def setUp(self):
        self.sprite = Sprite('flags',
            images=[
                ('brazil', get_absolute_path('country/flags/bra.png')),
                ('usa', get_absolute_path('country/flags/usa.png')),
                ('canada', get_absolute_path('country/flags/can.png')),
            ],
            packing_class=VerticalPacking
        )

    def test_name(self):
        self.assertEqual('flags', self.sprite.name)

    def test_css_class(self):
        self.assertEqual('sprite-flags', self.sprite.css_class)

    def test_dimensions(self):
        self.assertEqual(48, self.sprite.width)
        self.assertEqual(3 * 48, self.sprite.height)

    def test_sprite_css(self):
        css = self.sprite.generate_css('image_url.png')
        self.assertTrue(isinstance(css, basestring))
        self.assertTrue('.sprite-flags' in css)
        self.assertTrue('.sprite-flags-brazil{background-position:-0px -0px}' in css)
        self.assertTrue('.sprite-flags-usa{background-position:-0px -48px}' in css)
        self.assertTrue('.sprite-flags-canada{background-position:-0px -96px}' in css)


class BinSpriteTestCase(TestCase, SpriteTestCaseMixin):

    def setUp(self):
        self.sprite = Sprite('flags',
            images=[
                ('brazil', get_absolute_path('country/flags/bra.png')),
                ('usa', get_absolute_path('country/flags/usa.png')),
                ('canada', get_absolute_path('country/flags/can.png')),
            ],
            packing_class=BinPacking
        )

    def test_name(self):
        self.assertEqual('flags', self.sprite.name)

    def test_css_class(self):
        self.assertEqual('sprite-flags', self.sprite.css_class)

    def test_dimensions(self):
        self.assertEqual(96, self.sprite.width)
        self.assertEqual(96, self.sprite.height)

    def test_sprite_css(self):
        css = self.sprite.generate_css('image_url.png')
        self.assertTrue(isinstance(css, basestring))
        self.assertTrue('.sprite-flags' in css)
        self.assertTrue('.sprite-flags-brazil{background-position:-0px -0px}' in css)
        self.assertTrue('.sprite-flags-usa{background-position:-48px -0px}' in css)
        self.assertTrue('.sprite-flags-canada{background-position:-0px -48px}' in css)

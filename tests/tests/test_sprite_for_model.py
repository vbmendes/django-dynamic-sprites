# coding: utf8

from django.test import TestCase

from dynamic_sprites.model_sprite import ModelSprite
from tests.models import Country

from helpers import SpriteTestCaseMixin


class SpriteForEmptyQuerysetTestCase(TestCase, SpriteTestCaseMixin):

    def setUp(self):
        self.name = 'country'
        self.qs = Country.objects.none()
        self.image_field = 'flag'
        self.slug_field = 'slug'
        self.sprite = ModelSprite(
            name=self.name,
            queryset=self.qs,
            image_field=self.image_field,
            slug_field=self.slug_field
        )

    def tearDown(self):
        pass

    def test_sprite_for_empty_queryset_is_image_1x1(self):
        self.assertEqual(1, self.sprite.width)
        self.assertEqual(1, self.sprite.height)

    def test_sprite_name_is_country(self):
        self.assertEqual(self.name, self.sprite.name)

    def test_sprite_css(self):
        css = self.sprite.generate_css('image_url.png')
        self.assertTrue(isinstance(css, basestring))
        self.assertTrue('.sprite-country' in css)


class SpriteForQuerysetWithDataTestCase(TestCase, SpriteTestCaseMixin):

    fixtures = ['countries.json']

    def setUp(self):
        self.name = 'country'
        self.qs = Country.objects.all()
        self.image_field = 'flag'
        self.slug_field = 'slug'
        self.sprite = ModelSprite(
            name=self.name,
            queryset=self.qs,
            image_field=self.image_field,
            slug_field=self.slug_field
        )

    def test_sprite_for_queryset_with_data_dimensions(self):
        self.assertEqual(476 + 475, self.sprite.width)
        self.assertEqual(335, self.sprite.height)

    def test_sprite_css(self):
        css = self.sprite.generate_css('image_url.png')
        self.assertTrue(isinstance(css, basestring))
        self.assertIn('.sprite-country', css)
        self.assertIn('.sprite-country-brazil{background-position:-0px -0px}', css)
        self.assertIn('.sprite-country-usa{background-position:-476px -0px}', css)

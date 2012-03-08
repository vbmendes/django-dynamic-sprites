# coding: utf8

import os

from django.conf import settings
from django.db.models.signals import post_save
from django.test import TestCase

from dynamic_sprites.image import Image
from dynamic_sprites.listeners import ModelSpriteListener
from tests.models import Country


class ModelSpriteListenerSavingAnObjectInQuerysetTestCase(object):

    def setUp(self):
        self.name = 'listener-sprite'
        listener = ModelSpriteListener(
            name=self.name,
            queryset=Country.objects.all(),
            image_field='flag',
            slug_field='slug',
        )
        post_save.connect(listener, sender=Country)
        self.new_country = Country(
            name="Canada",
            flag='country/flags/can.png',
            slug='canada'
        )
        self.new_country.save()
        self.image_path = os.path.join(settings.MEDIA_ROOT, self.name + ".png")
        self.css_path = os.path.join(settings.MEDIA_ROOT, self.name + ".css")

    def tearDown(self):
        self.new_country.delete()
        if os.path.exists(self.image_path):
            os.remove(self.image_path)
        if os.path.exists(self.css_path):
            os.remove(self.css_path)

    def test_saving_an_object_creates_a_new_sprite_image(self):
        self.assertTrue(os.path.exists(self.image_path))

    def test_saving_an_object_creates_a_new_sprite_image_with_the_objects_image_dimensions(self):
        image = Image(self.image_path)
        self.assertEqual(48, image.width)
        self.assertEqual(48, image.height)

    def test_saving_an_object_creates_a_new_sprite_css(self):
        self.assertTrue(os.path.exists(self.css_path))

    def test_saving_an_object_creates_a_new_sprite_css_with_the_expected_style(self):
        with open(self.css_path, 'r') as f:
            css = f.read()
        self.assertTrue(isinstance(css, basestring))
        self.assertIn('.sprite-%s' % self.name, css)
        self.assertIn('.sprite-%s-%s{background-position:-0px -0px}' % (self.name, self.new_country.slug), css)


class ModelSpriteListenerUnderstandsQuerysetFromInstanceTestCase(TestCase):

    def setUp(self):
        self.name = 'listener-sprite'
        listener = ModelSpriteListener(
            name=self.name,
            image_field='flag',
            slug_field='slug',
        )
        post_save.connect(listener, sender=Country)
        self.new_country = Country(
            name="Canada",
            flag='country/flags/can.png',
            slug='canada'
        )
        self.new_country.save()
        self.image_path = os.path.join(settings.MEDIA_ROOT, self.name + ".png")
        self.css_path = os.path.join(settings.MEDIA_ROOT, self.name + ".css")

    def tearDown(self):
        self.new_country.delete()
        if os.path.exists(self.image_path):
            os.remove(self.image_path)
        if os.path.exists(self.css_path):
            os.remove(self.css_path)

    def test_saving_an_object_creates_a_new_sprite_image(self):
        self.assertTrue(os.path.exists(self.image_path))

    def test_saving_an_object_creates_a_new_sprite_image_with_the_objects_image_dimensions(self):
        image = Image(self.image_path)
        self.assertEqual(48, image.width)
        self.assertEqual(48, image.height)

    def test_saving_an_object_creates_a_new_sprite_css(self):
        self.assertTrue(os.path.exists(self.css_path))

    def test_saving_an_object_creates_a_new_sprite_css_with_the_expected_style(self):
        with open(self.css_path, 'r') as f:
            css = f.read()
        self.assertTrue(isinstance(css, basestring))
        self.assertIn('.sprite-%s' % self.name, css)
        self.assertIn('.sprite-%s-%s{background-position:-0px -0px}' % (self.name, self.new_country.slug), css)


class ModelSpriteListenerSavingAnObjectNotInQuerysetTestCase(object):

    def setUp(self):
        self.name = 'listener-sprite'
        listener = ModelSpriteListener(
            name=self.name,
            queryset=Country.objects.filter(slug='brazil'),
            image_field='flag',
            slug_field='slug',
        )
        post_save.connect(listener, sender=Country)
        self.new_country = Country(
            name="Canada",
            flag='country/flags/can.png',
            slug='canada'
        )
        self.new_country.save()
        self.image_path = os.path.join(settings.MEDIA_ROOT, self.name + ".png")
        self.css_path = os.path.join(settings.MEDIA_ROOT, self.name + ".css")

    def tearDown(self):
        self.new_country.delete()
        if os.path.exists(self.image_path):
            os.remove(self.image_path)
        if os.path.exists(self.css_path):
            os.remove(self.css_path)

    def test_saving_an_object_that_is_not_in_queryset_dont_create_image(self):
        self.assertFalse(os.path.exists(self.image_path))

    def test_saving_an_object_that_is_not_in_queryset_dont_create_css(self):
        self.assertFalse(os.path.exists(self.css_path))

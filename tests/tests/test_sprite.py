from django.test import TestCase

from dynamic_sprites.sprite import Sprite

class SpriteTestCase(TestCase):

    def setUp(self):
        self.sprite = Sprite('flags',
            images=[
                ('brazil', 'country/flags/brazil.gif'),
                ('usa', 'country/flags/usa.jpg'),
            ],
            packing=Sprite.HORIZONTAL
        )

    def test_name(self):
        self.assertEqual('flags', self.sprite.name)
    
    def test_css_class(self):
        self.assertEqual('sprite-flags', self.sprite.css_class)
    
    def test_dimensions(self):
        self.assertEqual(475 + 476, self.sprite.width)
        self.assertEqual(max(335, 330), self.sprite.height)

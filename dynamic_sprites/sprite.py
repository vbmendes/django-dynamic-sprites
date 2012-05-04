# -*- coding: utf-8 -*-

from dynamic_sprites.image import Image, OutputImage
from dynamic_sprites.output_css import OutputCss
from dynamic_sprites.packing import HorizontalPacking, EmptyPacking


class Sprite(object):

    def __init__(self, name, images, packing_class=HorizontalPacking):
        self.name = name
        self.images = self._load_images(images)
        if not images:
            packing_class = EmptyPacking
        self.packing = packing_class([img for name, img in self.images])

    def _load_images(self, images):
        return [(name, Image(path)) for name, path in images]

    @property
    def css_class(self):
        return 'sprite-%s' % self.name

    @property
    def width(self):
        return self.packing.width

    @property
    def height(self):
        return self.packing.height

    def generate(self):
        output = OutputImage(self.width, self.height)
        for name, image in self.images:
            pos = self.packing.get_image_position(image)
            output.add(image, pos.x, pos.y)
        return output

    def generate_css(self, image_url):
        output_parts = [".sprite-%(sprite_name)s{background-image:url(%(image_url)s)}" % {
            'sprite_name': self.name,
            'image_url': image_url,
        }]
        for name, image in self.images:
            pos = self.packing.get_image_position(image)
            output_parts.append(".sprite-%(sprite_name)s-%(name)s{background-position:-%(x)spx -%(y)spx}" % {
                'sprite_name': self.name,
                'name': name,
                'x': pos.x,
                'y': pos.y,
            })
        return OutputCss(' '.join(output_parts))

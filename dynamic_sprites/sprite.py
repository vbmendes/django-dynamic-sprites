
from PIL import Image as PImage

from dynamic_sprites.packing import HorizontalPacking, VerticalPacking, \
                                    BinPacking
from dynamic_sprites.image import Image, OutputImage


class Sprite(object):
    
    # BIN: http://codeincomplete.com/posts/2011/5/7/bin_packing/
    
    def __init__(self, name, images, packing_class=HorizontalPacking):
        self.name = name
        self.images = self._load_images(images)
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
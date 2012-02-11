
from dynamic_sprites.image import Image

class Sprite(object):
    
    # BIN: http://codeincomplete.com/posts/2011/5/7/bin_packing/
    HORIZONTAL, VERTICAL, BIN = range(3)
    
    def __init__(self, name, images, packing=None):
        self.name = name
        self.images = self._load_images(images)
        self.packing = packing
    
    def _load_images(self, images):
        return [(name, Image(path)) for name, path in images]
    
    @property
    def css_class(self):
        return 'sprite-%s' % self.name
    
    @property
    def width(self):
        if self.packing == Sprite.HORIZONTAL:
            method = sum
        return method(img[1].width for img in self.images)
    
    @property
    def height(self):
        if self.packing == Sprite.HORIZONTAL:
            method = max
        return method(img[1].height for img in self.images)
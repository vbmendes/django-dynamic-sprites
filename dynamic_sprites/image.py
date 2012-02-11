import os
from PIL import Image as PImage

from django.conf import settings

from dynamic_sprites.utils import cached_property


class Image(object):
    
    def __init__(self, path):
        self.path = path
    
    @property
    def width(self):
        return self.raw.size[0]
    
    @property
    def height(self):
        return self.raw.size[1]
    
    @property
    def maxside(self):
        return max(self.width, self.height)
    
    @property
    def area(self):
        return self.width * self.height
    
    @cached_property
    def raw(self):
        return self._load_raw()
    
    def _load_raw(self):
        with open(self.absolute_path, 'rb') as image_file:
            raw = PImage.open(image_file)
            raw.load()
        return raw
    
    @property
    def filename(self):
        return self.absolute_path.rsplit('.', 1)[0]
    
    @property
    def format(self):
        return self.absolute_path.rsplit('.', 1)[1]
    
    @property
    def absolute_path(self):
        return os.path.join(settings.MEDIA_ROOT, self.path)
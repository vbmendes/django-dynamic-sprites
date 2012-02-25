import os
from PIL import Image as PImage

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
        with open(self.path, 'rb') as image_file:
            raw = PImage.open(image_file)
            raw.load()
        return raw
    
    @property
    def filename(self):
        return self.path.rsplit('.', 1)[0].split('/')[-1]
    
    @property
    def format(self):
        return self.path.rsplit('.', 1)[1]


class OutputImage(object):
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.canvas = PImage.new('RGBA', (width, height), (0, 0, 0, 0))
    
    def add(self, image, x, y):
        self.canvas.paste(image.raw, (x, y))
    
    def save(self, path):
        self.canvas.save(   path, optimize=True)
    
    
        
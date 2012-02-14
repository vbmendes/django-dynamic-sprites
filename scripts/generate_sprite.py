#!/usr/bin/env python
# coding: utf8

from optparse import OptionParser, OptionGroup
import os
import sys

from dynamic_sprites.sprite import Sprite
from dynamic_sprites.packing import PACKING_DICT


def get_image_slug(image_path):
    return '.'.join(image_path.split('/')[-1].split('.')[:-1]).replace('-', '_')


def get_images(input_dir):
    images_paths = (os.path.join(input_dir, fname) for fname in os.listdir(input_dir))

    images = [(get_image_slug(image_path), image_path) for image_path in images_paths]
    
    return images
    

def main():
    parser = OptionParser(usage=("usage: %prog [options] source_dir output_path"))
    parser.add_option("-p", "--packing", dest="packing",  default='horizontal',
                      help="packing algorithm to generate sprites. Options are horizontal, vertical or bin")
    
    
    (options, args) = parser.parse_args()
    packing = PACKING_DICT[options.packing]
    
    input_dir = args[0]
    output_path = args[1]
    output_png_path = output_path + '.png'
    output_css_path = output_path + '.css'

    sprite = Sprite(name='test', images=get_images(input_dir), packing_class=packing)

    output_image = sprite.generate()
    output_css = sprite.generate_css(output_png_path)
    output_image.save(output_png_path)
    with open(output_css_path, 'w') as f:
        f.write(output_css+'\n')

if __name__ == '__main__':
    main()

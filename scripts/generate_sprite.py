#!/usr/bin/env python
# coding: utf8

from optparse import OptionParser
import os

from dynamic_sprites.packing import PACKING_DICT
from dynamic_sprites.slugify import slugify
from dynamic_sprites.sprite import Sprite


def get_image_slug(image_path):
    return slugify('.'.join(image_path.split('/')[-1].split('.')[:-1]))


def get_images(input_dir):
    images_paths = (os.path.join(input_dir, fname) for fname in os.listdir(input_dir))

    images = [(get_image_slug(image_path), image_path) for image_path in images_paths]

    return images


def main():
    parser = OptionParser(usage=("usage: %prog [options] source_dir output_path"))
    parser.add_option("-p", "--packing", dest="packing",  default='horizontal',
                      help="packing algorithm to generate sprites. Options are horizontal, vertical or bin")
    parser.add_option("-q", action="store_true", dest="pngquant")

    (options, args) = parser.parse_args()
    packing = PACKING_DICT[options.packing.strip()]

    input_dir = args[0]
    output_path = args[1]
    output_png_path = output_path + '.png'
    output_css_path = output_path + '.css'

    name = output_path.split('/')[-1]

    sprite = Sprite(name=name, images=get_images(input_dir), packing_class=packing)

    output_image = sprite.generate()
    output_css = sprite.generate_css(output_png_path)
    output_image.save(output_png_path, pngquant=options.pngquant)
    output_css.save(output_css_path)

if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-

import unittest

from dynamic_sprites.image import Image
from dynamic_sprites.packing import BinPacking

from helpers import MockedImage, get_absolute_path


class BinPackingBaseTestCase(object):

    def test_root_of_tree(self):
        self.assertEquals(0, self.bin_packing.tree.root.x)
        self.assertEquals(0, self.bin_packing.tree.root.y)
        self.assertEquals(self.bin_packing.width, self.bin_packing.tree.root.width)
        self.assertEquals(self.bin_packing.height, self.bin_packing.tree.root.height)


class BinPackingWithOneImageTestCase(unittest.TestCase, BinPackingBaseTestCase):

    def setUp(self):
        self.image = MockedImage()
        self.image.width = 10
        self.image.height = 20
        self.image.maxside = 20
        self.image.area = 200
        self.bin_packing = BinPacking(images=[self.image])

    def test_dimensions(self):
        self.assertEquals(self.image.width, self.bin_packing.width)
        self.assertEquals(self.image.height, self.bin_packing.height)


class BinPackingWithTwoImagesTestCase(unittest.TestCase, BinPackingBaseTestCase):

    def setUp(self):
        self.image1 = MockedImage()
        self.image1.width = 10
        self.image1.height = 20
        self.image1.maxside = 20
        self.image1.area = 200

        self.image2 = MockedImage()
        self.image2.width = 15
        self.image2.height = 15
        self.image2.maxside = 15
        self.image2.area = 15 * 15

        self.bin_packing = BinPacking(images=[self.image1, self.image2])

    def test_dimensions(self):
        self.assertEquals(25, self.bin_packing.width)
        self.assertEquals(20, self.bin_packing.height)

    def test_image1_position(self):
        self.assertEquals(0, self.bin_packing.get_image_position(self.image1).x)
        self.assertEquals(0, self.bin_packing.get_image_position(self.image1).y)

    def test_image2_position(self):
        self.assertEquals(10, self.bin_packing.get_image_position(self.image2).x)
        self.assertEquals(0, self.bin_packing.get_image_position(self.image2).y)


class BinPackingWithTwoUnorderedImagesTestCase(unittest.TestCase, BinPackingBaseTestCase):

    def setUp(self):
        self.image1 = MockedImage()
        self.image1.width = 10
        self.image1.height = 20
        self.image1.maxside = 20
        self.image1.area = 200

        self.image2 = MockedImage()
        self.image2.width = 30
        self.image2.height = 40
        self.image2.maxside = 40
        self.image2.area = 1200

        self.bin_packing = BinPacking(images=[self.image1, self.image2])

    def test_dimensions(self):
        self.assertEquals(40, self.bin_packing.width)
        self.assertEquals(40, self.bin_packing.height)

    def test_image1_position(self):
        self.assertEquals(30, self.bin_packing.get_image_position(self.image1).x)
        self.assertEquals(0, self.bin_packing.get_image_position(self.image1).y)

    def test_image2_position(self):
        self.assertEquals(0, self.bin_packing.get_image_position(self.image2).x)
        self.assertEquals(0, self.bin_packing.get_image_position(self.image2).y)


class BinPackingWidthThreeImages(unittest.TestCase, BinPackingBaseTestCase):

    def setUp(self):
        self.image1 = MockedImage()
        self.image1.width = 15
        self.image1.height = 20
        self.image1.maxside = 20
        self.image1.area = 300

        self.image2 = MockedImage()
        self.image2.width = 30
        self.image2.height = 40
        self.image2.maxside = 40
        self.image2.area = 1200

        self.image3 = MockedImage()
        self.image3.width = 15
        self.image3.height = 20
        self.image3.maxside = 20
        self.image3.area = 300

        self.bin_packing = BinPacking(images=[self.image1, self.image2, self.image3])

    def test_dimensions(self):
        self.assertEquals(45, self.bin_packing.width)
        self.assertEquals(40, self.bin_packing.height)

    def test_image1_position(self):
        self.assertEquals(30, self.bin_packing.get_image_position(self.image1).x)
        self.assertEquals(0, self.bin_packing.get_image_position(self.image1).y)

    def test_image2_position(self):
        self.assertEquals(0, self.bin_packing.get_image_position(self.image2).x)
        self.assertEquals(0, self.bin_packing.get_image_position(self.image2).y)

    def test_image3_position(self):
        self.assertEquals(30, self.bin_packing.get_image_position(self.image3).x)
        self.assertEquals(20, self.bin_packing.get_image_position(self.image3).y)


class BinPackingWithThreeImages(unittest.TestCase, BinPackingBaseTestCase):

    def setUp(self):
        self.image1 = MockedImage()
        self.image1.width = 10
        self.image1.height = 20
        self.image1.maxside = 20
        self.image1.area = 200

        self.image2 = MockedImage()
        self.image2.width = 30
        self.image2.height = 40
        self.image2.maxside = 40
        self.image2.area = 1200

        self.image3 = MockedImage()
        self.image3.width = 20
        self.image3.height = 20
        self.image3.maxside = 20
        self.image3.area = 400

        self.bin_packing = BinPacking(images=[self.image1, self.image2, self.image3])

    def test_dimensions(self):
        self.assertEquals(50, self.bin_packing.width)
        self.assertEquals(40, self.bin_packing.height)

    def test_image1_position(self):
        self.assertEquals(30, self.bin_packing.get_image_position(self.image1).x)
        self.assertEquals(20, self.bin_packing.get_image_position(self.image1).y)

    def test_image2_position(self):
        self.assertEquals(0, self.bin_packing.get_image_position(self.image2).x)
        self.assertEquals(0, self.bin_packing.get_image_position(self.image2).y)

    def test_image3_position(self):
        self.assertEquals(30, self.bin_packing.get_image_position(self.image3).x)
        self.assertEquals(0, self.bin_packing.get_image_position(self.image3).y)


class BinPackingWithThreeRealImages(unittest.TestCase, BinPackingBaseTestCase):

    def setUp(self):
        self.image1 = Image(get_absolute_path('country/flags/bra.png'))
        self.image2 = Image(get_absolute_path('country/flags/can.png'))
        self.image3 = Image(get_absolute_path('country/flags/usa.png'))
        self.bin_packing = BinPacking(images=[self.image1, self.image2, self.image3])

    def test_dimensions(self):
        self.assertEquals(96, self.bin_packing.width)
        self.assertEquals(96, self.bin_packing.height)

    def test_image1_position(self):
        self.assertEquals(0, self.bin_packing.get_image_position(self.image1).x)
        self.assertEquals(0, self.bin_packing.get_image_position(self.image1).y)

    def test_image2_position(self):
        self.assertEquals(48, self.bin_packing.get_image_position(self.image2).x)
        self.assertEquals(0, self.bin_packing.get_image_position(self.image2).y)

    def test_image3_position(self):
        self.assertEquals(0, self.bin_packing.get_image_position(self.image3).x)
        self.assertEquals(48, self.bin_packing.get_image_position(self.image3).y)


class BinPackingWithThreeRealImages(unittest.TestCase, BinPackingBaseTestCase):

    def setUp(self):
        self.image1 = Image(get_absolute_path('country/flags/bra.png'))
        self.image2 = Image(get_absolute_path('country/flags/can.png'))
        self.image3 = Image(get_absolute_path('country/flags/usa.png'))
        self.bin_packing = BinPacking(images=[self.image1, self.image2, self.image3])

    def test_dimensions(self):
        self.assertEquals(96, self.bin_packing.width)
        self.assertEquals(96, self.bin_packing.height)

    def test_image1_position(self):
        self.assertEquals(0, self.bin_packing.get_image_position(self.image1).x)
        self.assertEquals(0, self.bin_packing.get_image_position(self.image1).y)

    def test_image2_position(self):
        self.assertEquals(48, self.bin_packing.get_image_position(self.image2).x)
        self.assertEquals(0, self.bin_packing.get_image_position(self.image2).y)

    def test_image3_position(self):
        self.assertEquals(0, self.bin_packing.get_image_position(self.image3).x)
        self.assertEquals(48, self.bin_packing.get_image_position(self.image3).y)

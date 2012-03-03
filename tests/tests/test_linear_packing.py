import unittest

from dynamic_sprites.packing import AbstractLinearPacking, HorizontalPacking, VerticalPacking

from helpers import MockedImage


class LinearPackingTestCase(unittest.TestCase):

    def test_pure_linear_packing_raises_error(self):
        self.image = MockedImage()
        self.image.width = 10
        self.image.height = 20
        self.image.maxside = 20
        self.image.area = 200
        self.packing = AbstractLinearPacking(images=[self.image])
        self.assertRaises(ValueError, self.packing.get_image_position, self.image)
        self.assertRaises(ValueError, getattr, self.packing, 'width')
        self.assertRaises(ValueError, getattr, self.packing, 'height')


class HorizontalPackingWithOneImageTestCase(unittest.TestCase):

    def setUp(self):
        self.image = MockedImage()
        self.image.width = 10
        self.image.height = 20
        self.image.maxside = 20
        self.image.area = 200
        self.packing = HorizontalPacking(images=[self.image])

    def test_dimensions(self):
        self.assertEquals(self.image.width, self.packing.width)
        self.assertEquals(self.image.height, self.packing.height)

    def test_image_position(self):
        self.assertEquals(0, self.packing.get_image_position(self.image).x)
        self.assertEquals(0, self.packing.get_image_position(self.image).y)


class HorizontalPackingWithTwoImagesTestCase(unittest.TestCase):

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

        self.packing = HorizontalPacking(images=[self.image1, self.image2])

    def test_dimensions(self):
        self.assertEquals(25, self.packing.width)
        self.assertEquals(20, self.packing.height)

    def test_image1_position(self):
        self.assertEquals(0, self.packing.get_image_position(self.image1).x)
        self.assertEquals(0, self.packing.get_image_position(self.image1).y)

    def test_image2_position(self):
        self.assertEquals(10, self.packing.get_image_position(self.image2).x)
        self.assertEquals(0, self.packing.get_image_position(self.image2).y)


class VerticalPackingWithOneImageTestCase(unittest.TestCase):

    def setUp(self):
        self.image = MockedImage()
        self.image.width = 10
        self.image.height = 20
        self.image.maxside = 20
        self.image.area = 200
        self.packing = VerticalPacking(images=[self.image])

    def test_dimensions(self):
        self.assertEquals(self.image.width, self.packing.width)
        self.assertEquals(self.image.height, self.packing.height)

    def test_image_position(self):
        self.assertEquals(0, self.packing.get_image_position(self.image).x)
        self.assertEquals(0, self.packing.get_image_position(self.image).y)


class VerticalPackingWithTwoImagesTestCase(unittest.TestCase):

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

        self.packing = VerticalPacking(images=[self.image1, self.image2])

    def test_dimensions(self):
        self.assertEquals(15, self.packing.width)
        self.assertEquals(35, self.packing.height)

    def test_image1_position(self):
        self.assertEquals(0, self.packing.get_image_position(self.image1).x)
        self.assertEquals(0, self.packing.get_image_position(self.image1).y)

    def test_image2_position(self):
        self.assertEquals(0, self.packing.get_image_position(self.image2).x)
        self.assertEquals(20, self.packing.get_image_position(self.image2).y)

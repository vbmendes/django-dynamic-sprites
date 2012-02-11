import unittest

from dynamic_sprites.packing import BinPacking

class MockedImage(object):
    pass

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
        self.bin_packing = BinPacking(images=[self.image])
    
    def test_dimensions(self):
        self.assertEquals(self.image.width, self.bin_packing.width)
        self.assertEquals(self.image.height, self.bin_packing.height)
    
    
class BinPackingWidthTwoImagesTestCase(unittest.TestCase):
    
    def setUp(self):
        self.image1 = MockedImage()
        self.image1.width = 10
        self.image1.height = 20
        
        self.image2 = MockedImage()
        self.image2.width = 15
        self.image2.height = 15
        
        self.bin_packing = BinPacking(images=[self.image1, self.image2])
    
    def test_dimensions(self):
        self.assertEquals(25, self.bin_packing.width)
        self.assertEquals(20, self.bin_packing.height)

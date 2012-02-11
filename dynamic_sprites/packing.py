from dynamic_sprites.utils import cached_property

class BinNode(object):
    
    def __init__(self, x=0, y=0, width=0, height=0, used=False, down=None, right=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.used = used
        self.right = right
        self.down = down
        
    def __repr__(self):
        return '<dynamic_sprites.packing.BinNode x: %s y: %s w: %s h:%s>' % (self.x, self.y, self.width, self.height)
    
    def split(self, width, height):
        self.used = True
        self.down = BinNode(x=self.x,
                         y=self.y+height,
                         width=self.width, 
                         height=self.height-height)
        self.right = BinNode(x=self.x+width,
                          y=self.y,
                          width=self.width-width,
                          height=self.height)
        return self
        


class BinTree(object):
    
    def __init__(self, images):
        self.image_nodes = {}
        self.root = BinNode(width=images[0].width, height=images[0].height)
        for image in images:
            node = self.find(self.root, image.width, image.height)
            if node:
                node = node.split(image.width, image.height)
            else:
                node = self.grow(image.width, image.height)
            self.image_nodes[image] = node
    
    def find(self, node, width, height):
        if node.used:
            found_node = self.find(node.right, width, height) or \
                   self.find(node.down, width, height)
        elif node.width >= width and node.height >= height:
            found_node = node
        else:
            found_node = None
        return found_node

    def grow(self, width, height):
        method = self._define_grow_method(width, height)

        if method:
            node = method(width, height)
        else:
            node = None

        return node

    def _define_grow_method(self, width, height):
        can_grow_d = width <= self.width
        can_grow_r = height <= self.height
        should_grow_r = can_grow_r and self.height >= (self.width + width)
        should_grow_d = can_grow_d and self.width >= (self.height + height)

        if should_grow_r:
            method = self.grow_right
        elif should_grow_d:
            method = self.grow_down
        elif can_grow_r:
            method = self.grow_right
        elif can_grow_d:
            method = self.grow_down
        else:
            method = None

        return method

    def grow_right(self, width, height):
        self.root.right = BinNode(x=self.width,
                                  y=0,
                                  width=width,
                                  height=self.height)
        self.root.width += width
        node = self.find(self.root, width, height)
        if node:
            node = node.split(width, height)
        else:
            node = None
        return node
        

    def grow_down(self, width, height):
        self.root.right = BinNode(x=0,
                                  y=self.height,
                                  width=self.width,
                                  height=height)
        self.root.height += height
        node = self.find(self.root, width, height)
        if node:
            node = node.split(width, height)
        else:
            node = None
        return node
    
    @property
    def width(self):
        return self.root.width
    
    @property
    def height(self):
        return self.root.height


class BinPacking(object):
    
    def __init__(self, images):
        self.images = images
    
    @property
    def width(self):
        return self.tree.width
    
    @property
    def height(self):
        return self.tree.height
    
    @cached_property
    def tree(self):
        return self._build_tree()
    
    def _build_tree(self):
        tree = BinTree(self.images)
        return tree

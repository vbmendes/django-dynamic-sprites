from operator import attrgetter

from dynamic_sprites.utils import cached_property


class BaseNode(object):
    def __init__(self, x=0, y=0, width=0, height=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class BinNode(BaseNode):
    def __init__(self, x=0, y=0, width=0, height=0, used=False, down=None, right=None):
        super(BinNode, self).__init__(x, y, width, height)
        self.used = used
        self.right = right
        self.down = down

    def __repr__(self):  # pragma: no cover
        return '<dynamic_sprites.packing.BinNode x: %s y: %s w: %s h:%s>' % (self.x, self.y, self.width, self.height)

    def split(self, width, height):
        self.used = True
        self.down = BinNode(x=self.x,
                         y=self.y + height,
                         width=self.width,
                         height=self.height - height)
        self.right = BinNode(x=self.x + width,
                          y=self.y,
                          width=self.width - width,
                          height=self.height)
        return self


class BinTree(object):
    def __init__(self, images):
        self.images_nodes = {}
        self.root = BinNode(width=images[0].width, height=images[0].height)
        for image in images:
            node = self.find(self.root, image.width, image.height)
            if node:
                node = node.split(image.width, image.height)
            else:
                node = self.grow(image.width, image.height)
            self.images_nodes[image] = node

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

    def get_node_for_image(self, image):
        return self.images_nodes[image]


class BasePacking(object):

    def __init__(self, images):
        self.images = self.sort_images(images)

    def sort_images(self, images):
        return sorted(images, key=attrgetter('maxside', 'area'), reverse=True)

    def get_image_position(self, image):  # pragma: no cover
        raise NotImplementedError

    @property
    def width(self):  # pragma: no cover
        raise NotImplementedError

    @property
    def height(self):  # pragma: no cover
        raise NotImplementedError


class EmptyPacking(BasePacking):
    # Empty packing must be 1x1 because it's impossible
    # to save images with 0 width or height

    @property
    def width(self):
        return 1

    @property
    def height(self):
        return 1


class BinPacking(BasePacking):

    # BIN: http://codeincomplete.com/posts/2011/5/7/bin_packing/

    def get_image_position(self, image):
        return self.tree.get_node_for_image(image)

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


class AbstractLinearPacking(BasePacking):

    HORIZONTAL, VERTICAL = 'h', 'v'

    orientation = None

    def get_image_position(self, image):
        return self.images_nodes[image]

    @cached_property
    def images_nodes(self):
        return self._calculate_images_nodes()

    def _calculate_images_nodes(self):
        images_nodes = {}
        if self.orientation == self.HORIZONTAL:
            delta_position_method = lambda x, y, image: (x + image.width, y)
        elif self.orientation == self.VERTICAL:
            delta_position_method = lambda x, y, image: (x, y + image.height)
        else:
            self._raise_orientation_error()

        x = 0
        y = 0
        for image in self.images:
            images_nodes[image] = BaseNode(x, y)
            x, y = delta_position_method(x, y, image)

        return images_nodes

    def _raise_orientation_error(self):
        raise ValueError(
            "Invalid orientation for LinearPacking: %s. " % (self.orientation) +
            "Only %s and %s permitted." % (self.HORIZONTAL, self.VERTICAL)
        )

    @property
    def width(self):
        widths_generator = (img.width for img in self.images)
        if self.orientation == self.HORIZONTAL:
            width = sum(widths_generator)
        elif self.orientation == self.VERTICAL:
            width = max(widths_generator)
        else:
            self._raise_orientation_error()
        return width

    @property
    def height(self):
        heights_generator = (img.height for img in self.images)
        if self.orientation == self.VERTICAL:
            height = sum(heights_generator)
        elif self.orientation == self.HORIZONTAL:
            height = max(heights_generator)
        else:
            self._raise_orientation_error()
        return height


class HorizontalPacking(AbstractLinearPacking):
    orientation = AbstractLinearPacking.HORIZONTAL


class VerticalPacking(AbstractLinearPacking):
    orientation = AbstractLinearPacking.VERTICAL

PACKING_DICT = {
    'horizontal': HorizontalPacking,
    'vertical': VerticalPacking,
    'bin': BinPacking,
}

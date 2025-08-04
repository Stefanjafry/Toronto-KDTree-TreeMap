"""
kdtree.py
=========

This module defines a KDTree data structure for efficient spatial querying of municipal tree records.
It supports tree construction, lookup, and nearest-neighbor search using geographic coordinates
(latitude, longitude), and is built specifically for 2D spatial data.

Key Classes and Functions:
--------------------------
- KDTree: Main class for recursively building and querying a KD Tree from a list of MunicipalTree objects.
- _KDTNode: Internal node structure storing a single MunicipalTree and pointers to left/right subtrees.
- argsort: Helper function for sorting indices of a list by value (used in median splitting).
- CustomUnpickler: Ensures compatibility when loading serialized KDTree objects via `pickle`.

Features:
---------
- O(log n) average-case nearest neighbor search
- Recursive construction using alternating split dimensions (lat/lon)
- Tree visualization via `display_tree()`
- Compatibility with doctest-based testing
- Modular OOP design integrated with `MunicipalTree`

Usage:
------
This module is intended to be imported by other modules (e.g., MapView, User_Code) but can also be run
standalone for testing:
"""


from __future__ import annotations
from typing import Optional
from tree_utilities import MunicipalTree, TreeReader
import math  # This may be useful here!
import pickle  # for test cases in doctests

class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if name == 'KDTree':
            return KDTree
        elif name == '_KDTNode':
            return _KDTNode  # Ensure _KDTNode is accessible here
        return super().find_class(module, name)
def argsort(seq: list[int]) -> list[int]:
    """Return the indices of values in a sequence
    such that the values at each index are
    in ascending order. You don't need to use this function,
    but it may be helpful to find median values
    and partition data sets when you implement the KDTree.
    >>> argsort([])
    []
    >>> argsort([3, 1, 2])
    [1, 2, 0]
    >>> argsort([8, 6, 7, 5, 3, 0, 9])
    [5, 4, 3, 1, 2, 0, 6]
    >>> argsort([-3, -1, -2])
    [0, 2, 1]
    >>> argsort([4, 2, 2, 3])
    [1, 2, 3, 0]
    """
    return sorted(range(len(seq)), key=seq.__getitem__)


class _KDTNode(object):
    """A node to store some data in a KD-tree. A KD-tree is a binary tree
    that will be built of these nodes.

    === Attributes ===
    Information stored in a node:
    _tree: The MunicipalTree tree that is stored in this node.
    _pivot: The pivot value of this node. At alternating levels of a KD tree,
            this will be a lon or lat coordinate. All nodes in the left subtree
            will have a value less than the pivot, and all nodes in the right subtree
            will have a value greater than the pivot.

    Children of this node:
    _left: the left subtree of this node.
    _right: the right subtree of this node.
    """
    _tree: MunicipalTree
    _pivot: float  # the pivot value of this node, this will be either the lon or lat coordinate
    _left: Optional[_KDTNode]
    _right: Optional[_KDTNode]

    def __init__(self, tree: MunicipalTree, pivot: float) -> None:
        """Initialize a new _KDTNode storing <tree>, with no left or right nodes. """
        self._tree = tree
        # all the nodes in the right subtree will have a value greater than the pivot
        self._pivot = pivot  # all the nodes in the left subtree will have a value less than the pivot
        self._left = None  # Initially pointing to nothing
        self._right = None  # Initially pointing to nothing

    @property
    def tree(self) -> MunicipalTree:
        return self._tree

    @property
    def left(self) -> _KDTNode:
        return self._left

    @property
    def right(self) -> _KDTNode:
        return self._right

    @property
    def pivot(self) -> float:
        return self._pivot


class KDTree:
    """A KDTree that stores information about MunicipalTrees.
    It is made up of _KDTNode objects, and each _KDTNode object
    contains a MunicipalTree object.

    === Attributes ===
    tree_data: The data about trees stored in this KDTree.
    """
    KDTree: _KDTNode  # the root of the KD tree

    def __init__(self, data: list[MunicipalTree]) -> None:
        """Initialize a new KD Tree (KDTree) using the input data.
        If <KDTree> is None, the KDTree is empty.
        """
        # build the tree from the treelist, starting at depth 0
        self.KDTree = self.build_tree(data, 0)

    def display_tree(self) -> None:
        lines, *_ = self._display_helper(self.KDTree)
        for line in lines:
            print(line)

    def _display_helper(self, node: _KDTNode) -> tuple[list[str], int, int, int]:
        # No child.
        if node.right is None and node.left is None:
            line = f'{round(float(node.tree.lat), 3)},{round(float(node.tree.lon), 3)}'
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if node.right is None:
            lines, n, p, x = self._display_helper(node.left)
            s = f'{round(float(node.tree.lat), 3)},{round(float(node.tree.lon), 3)}'
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '|' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if node.left is None:
            lines, n, p, x = self._display_helper(node.right)
            s = f'{round(float(node.tree.lat), 3)},{round(float(node.tree.lon), 3)}'
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '|' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self._display_helper(node.left)
        right, m, q, y = self._display_helper(node.right)
        s = f'{round(float(node.tree.lat), 3)},{round(float(node.tree.lon), 3)}'
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '|' + (n - x - 1 + u + y) * ' ' + '|' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2

    def build_tree(self, data: list[MunicipalTree], depth: int) -> Optional[_KDTNode]:
        """Build a KDTree from the input data. Build the tree using the median
        of the data at each level of the tree. The depth of the tree is used to
        determine whether to split the data by latitude or longitude.
        Split by latitude if depth is even, and by longitude if depth is odd.
        Your implementation will be recursive.
        >>> t = KDTree([MunicipalTree('1', '1', 'oak', '10', '1', '1'), MunicipalTree('2', '2', 'cherry', '10', '2', '2'), MunicipalTree('3', '3', 'maple', '10', '3', '3')])
        >>> t.display_tree() # doctest: +NORMALIZE_WHITESPACE
            ___2.0,2.0___
           |             |
        1.0,1.0       3.0,3.0
        """
        if not data:
            return None
        dim = depth % 2
        data.sort(key=lambda tree: (tree.lat, tree.lon)[dim])
        median_idx = len(data) // 2
        median_tree = data[median_idx]
        pivot = (median_tree.lat, median_tree.lon)[dim]
        node = _KDTNode(median_tree, pivot)
        node._left = self.build_tree(data[:median_idx], depth + 1)
        node._right = self.build_tree(data[median_idx + 1:], depth + 1)
        return node

    def lookup(self, lat: float, lon: float) -> bool:
        """Return True if there is a tree with the given latitude and longitude coordinated
        in the KDTree.
        >>> with open('data/kdtree.pkl', 'rb') as file: loaded_object = CustomUnpickler(file).load()
        >>> print(loaded_object.lookup(43.72412, -79.55176))
        True
        >>> print(loaded_object.lookup(44, -79))
        False
        """
        return self._lookup_recursive(self.KDTree, lat, lon, 0)

    def _lookup_recursive(self, node, lat, lon, depth):
        if node is None:
            return False
        if round(lat, 5) == round(node.tree.lat, 5) and round(lon, 5) == round(node.tree.lon, 5):
            return True
        dim = depth % 2
        pivot = node.pivot
        if (lat if dim == 0 else lon) < pivot:
            return self._lookup_recursive(node.left, lat, lon, depth + 1)
        else:
            return self._lookup_recursive(node.right, lat, lon, depth + 1)

    def get_nearest(self, lat: float, lon: float) -> Optional[MunicipalTree]:
        """ Return the nearest tree to the given latitude and longitude.
        >>> with open('data/kdtree.pkl', 'rb') as file: loaded_object = CustomUnpickler(file).load()
        >>> print(loaded_object.get_nearest(43.739,-79.552))
        Mulberry, white weeping at (43.739, -79.552) with diameter 1
        >>> print(loaded_object.get_nearest(43.752,-79.607))
        Birch, Colorado blue at (43.752, -79.607) with diameter 1
        """
        return self._get_nearest_recursive(self.KDTree, lat, lon, 0, (None, float('inf')))[0]

    def _get_nearest_recursive(self, node, lat, lon, depth, best):
        if node is None:
            return best
        dist = math.sqrt((node.tree.lat - lat) ** 2 + (node.tree.lon - lon) ** 2)
        if dist < best[1]:
            best = (node.tree, dist)
        dim = depth % 2
        pivot = node.pivot
        if (lat if dim == 0 else lon) < pivot:
            best = self._get_nearest_recursive(node.left, lat, lon, depth + 1, best)
        else:
            best = self._get_nearest_recursive(node.right, lat, lon, depth + 1, best)
        # Check other subtree if needed
        if (pivot - (lat if dim == 0 else lon)) ** 2 < best[1]:
            if (lat if dim == 0 else lon) < pivot:
                best = self._get_nearest_recursive(node.right, lat, lon, depth + 1, best)
            else:
                best = self._get_nearest_recursive(node.left, lat, lon, depth + 1, best)
        return best



if __name__ == '__main__':
    sys.modules['__main__'].KDTree = KDTree
    print("Below is an example of a KD Tree:")
    with open('data/kdtree.pkl', 'rb') as file:
        loaded_object = pickle.load(file)
        loaded_object.display_tree()

    # Once you write code to build your own KD Tree,
    # you can test it using the doctests below.
    import doctest
    doctest.testmod()

    # You can also test your implementation using the following code:
    trees = TreeReader.read_trees('data/tiny.csv')
    kd = KDTree(trees)
    kd.display_tree()







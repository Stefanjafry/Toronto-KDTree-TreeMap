"""
AutoTester: KDTree and MunicipalTree Unit Test Suite
=====================================================

This module provides unit tests for validating core components of the spatial tree mapping project,
including KDTree construction, nearest-neighbor lookup, Euclidean distance calculation, and helper utilities.

It supports modular test execution by toggling specific test flags at the top of the script.

Modules Tested:
---------------
- KDTree: Verifies tree construction, node layout, and nearest-neighbor search accuracy.
- MunicipalTree: Validates Euclidean distance logic for coordinate comparisons.
- argsort: Confirms correct ordering of index positions by value.

Dependencies:
-------------
- kdtree.py
- tree_utilities.py
- data/kdtree.pkl (prebuilt KDTree object for lookups)

Usage:
------
To run specific tests, set the corresponding test_* flags to True and execute the script.

Example:
    test_get_nearest = True
    python autotester.py
"""

from kdtree import KDTree, _KDTNode, argsort
from tree_utilities import MunicipalTree

import pickle  # for test cases in doctests

test_lookup = False
test_get_nearest = False
test_build_tree = False
test_argsort = False
test_distance = True


# lookup test
def test_lookup_fun():
    with open('data/kdtree.pkl', 'rb') as file:
        loaded_object = pickle.load(file)
        assert(loaded_object.lookup(43.72412, -79.55176))
        assert(not loaded_object.lookup(44, -79))
        assert(loaded_object.lookup(43.73912, -79.55236))


def test_get_nearest_fun():
    with open('data/kdtree.pkl', 'rb') as file:
        loaded_object = pickle.load(file)
        assert(loaded_object.get_nearest(43.72412, -79.55176).species == 'Yew')
        assert(loaded_object.get_nearest(43.73912, -79.5523).species == 'Mulberry, white weeping')
        assert(loaded_object.get_nearest(43.75480, -79.60098).species == 'Spruce, Colorado blue')


def test_build_tree_fun():
    t = KDTree([MunicipalTree('1', '1', 'oak', '10', '1', '1'), MunicipalTree('2', '2', 'cherry', '10', '2', '2'),
                     MunicipalTree('3', '3', 'maple', '10', '3', '3')])
    lines, *_ = t._display_helper(t.KDTree)
    correct = ['    ___2.0,2.0___    ', '   |             |   ', '1.0,1.0       3.0,3.0']
    i = 0
    for line in lines:
        assert(line == correct[i])
        i += 1


def test_argsort_fun():
    assert(argsort([3, 1, 2]) == [1, 2, 0])
    assert(argsort([8, 6, 7, 5, 3, 0, 9]) == [5, 4, 3, 1, 2, 0, 6])


def test_distance_fun():
    tree = MunicipalTree('1', '1', 'oak', '10', '1', '1')
    assert(tree.distance_to(1, 1) == 0)
    assert(tree.distance_to(2, 2) == 1.41421)
    assert(tree.distance_to(3, 3) == 2.82843)


if __name__ == '__main__':

    if test_lookup:
        test_lookup_fun()
    if test_argsort:
        test_argsort_fun()
    if test_get_nearest:
        test_get_nearest_fun()
    if test_build_tree:
        test_build_tree_fun()
    if test_distance:
        test_distance_fun()

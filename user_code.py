"""
user_code.py
============

This script serves as the main entry point for the interactive municipal tree mapping project.
It integrates all core components — tree loading, spatial indexing via KDTree, and interactive
visualization via MapView — into a complete application.

Functionality:
--------------
- Loads a pre-built KDTree from a pickle file (`data/kdtree.pkl`) and displays its structure
- Reads municipal tree data from `data/york_treelist.csv` using `TreeReader`
- Constructs a KDTree from the dataset
- Launches an interactive map window (`MapView`) where users can click to find the nearest tree

Components Used:
----------------
- KDTree: Spatial data structure for efficient nearest-neighbor queries
- MunicipalTree: Object representing a tree with coordinates, diameter, species, etc.
- TreeReader: Static utility class for reading tree data from CSV
- MapView: GUI that allows interactive exploration of the tree dataset

Usage:
------
Run this script directly to launch the interactive application:

Author:
Stefan Jafry, 2025
"""

from kdtree import KDTree, _KDTNode
from map_view import MapView
from tree_utilities import TreeReader
import pickle  # for test cases in doctests

# This code simply serves as an example of how to use the KDTree and MapView classes
# to create an interactive map of the trees in the treelist.
if __name__ == "__main__":

    print("Below is an example of a KD Tree:")
    with open('data/kdtree.pkl', 'rb') as file:
        loaded_object = pickle.load(file)
        loaded_object.display_tree()

    treelist = TreeReader.read_trees("data/york_treelist.csv")
    print("Read " + str(len(treelist)) + " trees from file.")

    kdtree = KDTree(treelist)  # build the tree from the treelist
    print("Built a KD tree.")

    # create an interactive map of the trees that allows the
    # user to click the information about the tree nearest to the click
    treeView = MapView(kdtree, treelist)
    treeView.draw()
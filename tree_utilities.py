"""
tree_utilities.py
=================

This module defines the core data structure used throughout the KDTree spatial mapping project:
the `MunicipalTree` class, which models a single municipal tree with relevant attributes such as
ID, location, species, and diameter.

It also includes a `TreeReader` utility class with static methods to read tree data from a CSV file
and return a list of `MunicipalTree` objects. These objects are later used for spatial indexing,
visualization, and nearest-neighbor queries via KDTree.

Classes:
--------
- MunicipalTree: Represents a tree in the dataset. Includes latitude/longitude attributes and methods
  to compute Euclidean distance to a target coordinate.
- TreeReader: A CSV utility that loads tree records and instantiates them as `MunicipalTree` objects.

Key Features:
-------------
- Clean object-oriented structure for tree data encapsulation
- Euclidean distance calculation with rounding to 5 decimal places
- Doctests for validation of distance logic and type consistency
- Static file reader that abstracts away CSV parsing logic

Usage:
------
This module is meant to be imported by KDTree, MapView, or testing modules.
However, when run directly, it will:
- Execute doctests for validation
- Attempt to read `data/york_treelist.csv` for demonstration

Example:
    from tree_utilities import TreeReader
    trees = TreeReader.read_trees("data/york_treelist.csv")
"""

from __future__ import annotations
import csv
import math  # you will need this to calculate distances!


class MunicipalTree:
    """A municipal tree
    === Attributes ===
    _id: The id of the tree
    _ward: The ward responsible for the tree
    _species: The species of the tree
    _diameter: The diameter of the tree
    _lon: longitude
    _lat: latitude
    """
    _id: int
    _ward: int
    _species: str
    _diameter: int
    _lon: float
    _lat: float

    def __init__(self, id: str, ward: str, species: str, diameter: str, lon: str, lat: str) -> None:
        """Initialize a new tree.
        >>> tree = MunicipalTree('1', '1', 'oak', '10', '1', '1')
        >>> isinstance(tree._id, int)
        True
        >>> isinstance(tree._ward, int)
        True
        >>> isinstance(tree._lon, float)
        True
        """
        self._id = int(id)
        self._ward = int(ward)
        self._species = species
        self._diameter = int(diameter)
        self._lon = float(lon)
        self._lat = float(lat)

    def __str__(self) -> str:
        """ Return a string representation of this tree.
        Format: <species> at (<longitude>, <latitude>) with diameter <diameter>
        """
        a = round(float(self._lat), 3)
        b = round(float(self._lon), 3)
        return f'{self._species} at ({a}, {b}) with diameter {self._diameter}'

    @property
    def lon(self) -> float:
        return self._lon

    @property
    def lat(self) -> float:
        return self._lat

    @property
    def species(self) -> str:
        return self._species

    def distance_to(self, lon: float, lat: float) -> float:
        """Return the distance from this tree to the given coordinates.
        Calculate the distance using the Euclidean distance formula,
        and round the result to 5 decimal places.
        >>> tree = MunicipalTree('1', '1', 'oak', '10', '1', '1')
        >>> tree.distance_to(1, 1)
        0.0
        >>> tree.distance_to(2, 2)
        1.41421
        >>> tree.distance_to(3,3)
        2.82843
        >>> tree = MunicipalTree('5216', '1', 'Yew', '1', '-79.551765', '43.724121')
        >>> tree.distance_to(-79.551765, 43.724121)
        0.0
        >>> tree.distance_to(-79.551865, 43.724221)
        0.00014
        >>> tree.distance_to(-79.554, 43.726)
        0.00292
        """
        distance = math.sqrt((lat - self._lat) ** 2 + (lon - self._lon) ** 2)
        return round(distance, 5)


class TreeReader:
    """A class to read the tree data from a csv file.
    We will use static methods to read the data,
    so there will be no need to create an instance of
    this class."""

    @staticmethod  # static! We do not need an instance of this class to use this method.
    def read_trees(filename: str) -> list[MunicipalTree]:
        """Read the tree data from the csv file and return a
        list of trees."""
        trees = []

        with open(filename, newline='') as csvfile:
            treereader = csv.reader(csvfile, delimiter=',')
            count = 0
            for row in treereader:
                if count > 0:
                    trees.append(MunicipalTree(*row))
                count += 1

        return trees


if __name__ == '__main__':
    # You can use this to test this portion of your code.
    import doctest
    doctest.testmod()
    trees = TreeReader.read_trees('data/york_treelist.csv')
    tree=MunicipalTree('','','','','','')

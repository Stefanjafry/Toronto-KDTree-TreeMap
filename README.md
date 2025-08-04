Toronto KDTree TreeMap:

This project implements an object-oriented spatial indexing system using a KD-Tree to efficiently query and visualize municipal tree data from the City of Toronto. It includes an interactive map interface that allows users to click on locations and retrieve the nearest tree based on geospatial coordinates.

Overview:

The application showcases:

A two-dimensional KD-Tree data structure implemented from scratch

Object-oriented design patterns for tree data, spatial querying, and visualization

A Model-View-Controller (MVC)-inspired architecture separating data modeling (KDTree, MunicipalTree) from visualization (MapView)

Interactive spatial querying using Matplotlib and event listeners

Key Components:

MunicipalTree: Represents a single tree with its ID, ward, species, diameter, and geolocation. Includes a method to compute Euclidean distance to a given point.

TreeReader: A static utility class to parse a CSV file and return a list of MunicipalTree instances.

KDTree: A 2D KD-Tree implementation that allows efficient nearest-neighbor search in spatial datasets. It recursively splits on alternating axes and stores the structure as a binary tree.

MapView: Uses matplotlib to render a map of Toronto, draw trees, and highlight the nearest one when the user clicks a location. Tightly integrates with KDTree to perform fast spatial queries.

user_code.py: Launches the program by reading data, building the KDTree, and starting the interactive map interface.

autotester.py: Contains test functions to validate correctness of nearest neighbor logic, distance calculations, KDTree structure, and sorting.

File Structure:

data/

york_treelist.csv : CSV file with tree data

york.png : Background image of the map

kdtree.pkl : (Optional) serialized KDTree for testing

autotester.py : Unit tests for core components
user_code.py : Main program launcher
kdtree.py : KDTree and internal node structure
map_view.py : Map visualization with spatial interactivity
tree_utilities.py : Data models and CSV loading
requirements.txt : Python dependencies
.gitignore : Files and directories excluded from Git tracking
README.md : Project documentation (this file)

Setup Instructions:

Clone the repository

git clone https://github.com/Stefanjafry/Toronto-KDTree-TreeMap.git
cd Toronto-KDTree-TreeMap

(Optional) Create and activate a virtual environment

python -m venv .venv
On Windows: .venv\Scripts\activate
On Mac/Linux: source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Running the Project

To launch the interactive KDTree map, run:

python user_code.py

You can then click on the Toronto map and the program will display the tree closest to the clicked location.

To run the built-in test suite:

python autotester.py

License:

This project is licensed under the MIT License. You are free to use, modify, and distribute the code.

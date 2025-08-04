"""
map_view.py
===========

This module implements the interactive map visualization component of the municipal tree
KDTree project. Using the `matplotlib` library, it provides a graphical interface where
users can click anywhere on a map of Toronto and retrieve the nearest municipal tree,
queried efficiently via a KDTree spatial index.

Classes:
--------
- MapView: A class that encapsulates the map interface and integrates with a KDTree to
  handle real-time nearest-neighbor queries triggered by mouse clicks.

Key Features:
-------------
- Displays municipal tree locations over a background map (`york.png`)
- Supports real-time user interaction via click events
- Converts pixel click coordinates to geographic coordinates (lat/lon)
- Efficiently queries the nearest tree using the KDTree structure
- Highlights the selected nearest tree dynamically

Design Pattern:
---------------
This module follows the **View** component of the **Model-View-Controller (MVC)** design:
- The KDTree (Model) handles the spatial data and nearest-neighbor logic
- MapView (View) renders the data and captures user input
- The controller logic is indirectly managed through mouse event bindings

Dependencies:
-------------
- matplotlib.pyplot
- matplotlib.image
- math
- kdtree.KDTree
- tree_utilities.MunicipalTree

Usage:
------
This module is intended to be imported and instantiated from `user_code.py` or another
controller script. It is **not designed to be executed directly**.

Example:
    kdtree = KDTree(TreeReader.read_trees("york_treelist.csv"))
    view = MapView(kdtree, treedata)
    view.draw()
"""
from __future__ import annotations
from kdtree import KDTree  # for building the KDTree
from tree_utilities import MunicipalTree  # for representing the trees in the dataset

import math  # for mathematical operations
import matplotlib.pyplot as plt  # for plotting
import matplotlib.image as mpimg
from matplotlib.backend_bases import PickEvent  # for handling mouse clicks


class MapView:
    """A map view of the trees in the dataset. The map view is responsible for
    drawing the map and the data on the map. It also handles mouse clicks on the map.
    """

    def __init__(self, kdtree: KDTree, treedata: list[MunicipalTree]) -> None:
        """Initialize a new map view. The map view is responsible for drawing
        the map and the data on the map. It also handles mouse clicks on the map.
        It contains a reference to the KDTree so that it can query the KDTree for
        the data point nearest to a mouse click.
        Attributes:
        _h: height of the map
        _w: width of the map
        _urx: upper right x coordinate of the map
        _ury: upper right y coordinate of the map
        _llx: lower left x coordinate of the map
        _lly: lower left y coordinate of the map
        _fig: the figure
        _ax: the axes
        _treelist: the list of trees to be visualized
        _kdtree: the kdtree, which facilitates nearest neighbor queries
        """
        self._h, self._w = 300, 670  # dimensions of the map
        self._urx, self._ury = 43.781322, -79.533667  # coordinate boundaries of the map
        self._llx, self._lly = 43.745431, -79.424748
        self._fig = None
        self._ax = None
        self._kdtree = kdtree  # the kdtree, which facilitates nearest neighbor queries
        self._treedata = treedata  # the list of trees

    def on_pick(self, event: PickEvent):
        """Handle a mouse click event on the map. This method will find the
        nearest item of data to the mouse click by calling the get_nearest method
        of the KD Tree. It will then draw a circle around that data point on the map."""
        xmouse, ymouse = event.mouseevent.xdata, event.mouseevent.ydata
        lon = self._lly + ((self._ury - self._lly) * (self._w - xmouse) / self._w)
        lat = self._llx + ((self._urx - self._llx) * (self._h - ymouse) / self._h)

        nearest = self._kdtree.get_nearest(lat, lon)
        print("\nThe nearest Municipal Tree is a:\n" + str(nearest))

        self.draw_trees([nearest], 'co')
        self._fig.canvas.draw()

    def draw(self):
        """Draw the map and the data on the map. This method will not return
        until the user has closed the map window."""
        self._fig, self._ax = plt.subplots()
        self.draw_map()
        self._fig.canvas.draw()
        self.draw_trees(self._treedata)
        self._fig.canvas.mpl_connect('pick_event', self.on_pick)
        plt.title('Municipal Trees in Toronto')
        plt.show()

    def draw_trees(self, trees: list[MunicipalTree], color='ro'):
        """Helper method for draw; draws the trees on the map."""
        ylim = self._ax.get_ylim()
        xlim = self._ax.get_xlim()
        self._h = math.floor(max(ylim))
        self._w = math.floor(max(xlim))

        # locate only the trees in the boundaries of the map
        filtered_trees = list(
            filter(lambda x: self._lly >= float(x._lon) >= self._ury and self._urx >= float(x._lat) >= self._llx,
                   trees))
        xvalues = list(
            map(lambda x: self._w - self._w * ((float(x._lon) - self._lly) / (self._ury - self._lly)), filtered_trees))
        yvalues = list(
            map(lambda x: self._h - self._h * ((float(x._lat) - self._llx) / (self._urx - self._llx)), filtered_trees))

        # draw the trees
        self._ax.plot(xvalues, yvalues, color, picker=True)

    def draw_map(self):
        """Helper method for draw; draws the map."""
        img = mpimg.imread('data/york.png')  # read the map image
        self._ax.imshow(img)
        self._ax.autoscale(False)


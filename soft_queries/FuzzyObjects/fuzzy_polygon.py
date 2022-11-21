from typing import List, Dict
from collections import OrderedDict

from qgis.core import (QgsGeometry, QgsWkbTypes)

from fuzzy_object import FuzzyObject


class FuzzyPolygon(FuzzyObject):

    geom_types: List[QgsWkbTypes.Type] = [QgsWkbTypes.Type.Polygon, QgsWkbTypes.Type.MultiPolygon]

    def __init__(self) -> None:
        super(FuzzyObject, self).__init__()


if __name__ == "__main__":

    a = FuzzyPolygon()
    geom = QgsGeometry.fromWkt("Polygon (0 0, 1 0, 1 1, 0 1, 0 0)")
    a.add_alpha_cut(1, geom)
    a.add_alpha_cut(0, geom.buffer(1, 8))
    a.add_alpha_cut(0.5, geom.buffer(0.5, 8))
    print(a._alpha_cuts.keys())
    print(a.find_lower_alpha(0.7))
    print(a.find_lower_alpha(0.3))
    print(a.find_lower_alpha(0.9))
    print(a.find_upper_alpha(0.4))
    print(a.find_upper_alpha(0.1))
    print(a.find_upper_alpha(0.9))

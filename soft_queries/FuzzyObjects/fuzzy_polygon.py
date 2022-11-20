from typing import List, Dict
from collections import OrderedDict

from qgis.core import (QgsGeometry, QgsWkbTypes)


class FuzzyPolygon:

    def __init__(self) -> None:
        self._alpha_cuts: OrderedDict[float, QgsGeometry] = OrderedDict({})

    @classmethod
    def from_data(cls, alphas: List[float], geometries: List[QgsGeometry]):

        if len(alphas) != len(geometries):
            raise ValueError("Both input lists must be of equal length.")

        polygon = cls()

        for i in range(len(alphas)):
            polygon.add_alpha_cut(alphas[i], geometries[i])

        return polygon

    def find_lower_alpha(self, alpha: float) -> float:
        return_key = None
        for key in self._alpha_cuts.keys():
            if key > alpha:
                break
            return_key = key
        return return_key

    def find_upper_alpha(self, alpha: float) -> float:
        return_key = None
        for key in reversed(self._alpha_cuts.keys()):
            if key < alpha:
                break
            return_key = key
        return return_key

    def add_alpha_cut(self, alpha: float, geometry: QgsGeometry) -> None:
        if not (0 <= alpha <= 1):
            raise ValueError("Alpha value needs to be from interval [0, 1].")

        if alpha in self._alpha_cuts.keys():
            raise ValueError("Alpha value already exists in the object.")

        if geometry.wkbType() not in [QgsWkbTypes.Type.Polygon, QgsWkbTypes.Type.MultiPolygon]:
            raise ValueError("Only type of geometry polygon is allowed.")

        self._alpha_cuts[alpha] = geometry

        self._alpha_cuts = OrderedDict(sorted(self._alpha_cuts.items()))

    def alpha_cut_contains(self, alpha: float, geom: QgsGeometry) -> bool:
        return self._alpha_cuts[alpha].contains(geom)

    def alpha_cut_is_contained(self, alpha: float, geom: QgsGeometry) -> bool:
        return geom.contains(self._alpha_cuts[alpha])


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

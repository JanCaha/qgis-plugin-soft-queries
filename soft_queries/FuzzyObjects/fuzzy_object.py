from typing import List, Dict
from collections import OrderedDict

from qgis.core import (QgsGeometry, QgsWkbTypes)


class FuzzyObject:

    geom_allowed_types: List[QgsWkbTypes.Type] = []

    def __init__(self) -> None:
        self._alpha_cuts: OrderedDict[float, QgsGeometry] = OrderedDict({})

    def is_empty(self) -> bool:
        return len(self._alpha_cuts) == 0

    def _check_geom_type(self, geom: QgsGeometry) -> bool:
        return geom in self.geom_allowed_types

    def _check_geom_type_all(self, geoms: List[QgsGeometry]) -> bool:
        types = [self._check_geom_type(geom) for geom in geoms]
        return all(types)

    def _check_alpha_cut_fits(self, alpha: float, geom: QgsGeometry) -> bool:
        if self.is_empty():
            return True

        if self.alpha_cut_is_contained()
    
    def lower_alpha(self, alpha: float) -> float:
        return_key = None
        for key in self._alpha_cuts.keys():
            if key > alpha:
                break
            return_key = key
        return return_key

    def upper_alpha(self, alpha: float) -> float:
        return_key = None
        for key in reversed(self._alpha_cuts.keys()):
            if key < alpha:
                break
            return_key = key
        return return_key
        
    @classmethod
    def from_data(cls, alphas: List[float], geometries: List[QgsGeometry]):

        if len(alphas) != len(geometries):
            raise ValueError("Both input lists must be of equal length.")

        polygon = cls()

        for i in range(len(alphas)):
            polygon.add_alpha_cut(alphas[i], geometries[i])

        return polygon

    def add_alpha_cut(self, alpha: float, geom: QgsGeometry) -> None:
        if not (0 <= alpha <= 1):
            raise ValueError("Alpha value needs to be from interval [0, 1].")

        if alpha in self._alpha_cuts.keys():
            raise ValueError("Alpha value already exists in the object.")

        if geom.wkbType() not in [QgsWkbTypes.Type.Polygon, QgsWkbTypes.Type.MultiPolygon]:
            raise ValueError("Only type of geometry polygon is allowed.")

        self._check_geom_type(geom)

        self._alpha_cuts[alpha] = geom

        self._alpha_cuts = OrderedDict(sorted(self._alpha_cuts.items()))

    def alpha_cut_contains(self, alpha: float, geom: QgsGeometry) -> bool:
        upper_alpha = self.upper_alpha(alpha)
        if upper_alpha:
            return geom.contains(self._alpha_cuts[upper_alpha])
        return True
    
    def alpha_cut_is_contained(self, alpha: float, geom: QgsGeometry) -> bool:
        lower_alpha = self.lower_alpha(alpha)
        if lower_alpha:
            return self._alpha_cuts[lower_alpha].clipped(geom)
        return True
    
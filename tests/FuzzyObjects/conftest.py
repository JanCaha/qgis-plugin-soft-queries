import pytest

from qgis.core import QgsGeometry

from soft_queries.FuzzyObjects import FuzzyPolygon


@pytest.fixture
def raster_layer_path() -> FuzzyPolygon:

    geom = QgsGeometry.fromWkt("Polygon ((0 0, 1 0, 1 1, 0 1, 0 0))")
    geoms = [
        geom,
        geom.buffer(1, 8),
        geom.buffer(0.5, 8),
        geom.buffer(0.75, 8),
        geom.buffer(0.25, 8)
    ]

    alphas = [1, 0, 0.5, 0.25, 0.75]

    fp = FuzzyPolygon.from_data(alphas, geoms)

    return fp

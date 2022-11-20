from qgis.core import QgsGeometry

from soft_queries.FuzzyObjects.fuzzy_polygon import FuzzyPolygon


def test_init():
    fp = FuzzyPolygon()
    assert isinstance(fp, FuzzyPolygon)


def test_create_from_list():
    geom = QgsGeometry.fromWkt("Polygon ((0 0, 1 0, 1 1, 0 1, 0 0))")
    geoms = [geom, geom.buffer(1, 8), geom.buffer(0.5, 8)]
    alphas = [1, 0, 0.5]

    fp = FuzzyPolygon.from_data(alphas, geoms)

    assert isinstance(fp, FuzzyPolygon)

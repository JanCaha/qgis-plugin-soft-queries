import pytest
from qgis.core import QgsProcessingContext, QgsProcessingFeedback, QgsVectorLayer

import soft_queries.utils as utils
from soft_queries.plugin_soft_queries import SoftQueriesPlugin
from tests.utils import data_path

pytest.register_assert_rewrite("assert_helpers")


@pytest.fixture
def raster_layer_path() -> str:
    return data_path("dsm_epsg_5514.tif")


@pytest.fixture
def feedback() -> QgsProcessingFeedback:
    return QgsProcessingFeedback()


@pytest.fixture
def context() -> QgsProcessingContext:
    return QgsProcessingContext()


@pytest.fixture
def raster_fuzzy_1_path() -> str:
    return data_path("fuzzy_1.tif")


@pytest.fixture
def raster_fuzzy_2_path() -> str:
    return data_path("fuzzy_2.tif")


@pytest.fixture(autouse=True, scope="session")
def init_plugin(qgis_iface) -> SoftQueriesPlugin:
    utils.add_deps_folder_to_path()

    plugin = SoftQueriesPlugin(qgis_iface)

    plugin.register_exp_functions()

    return plugin


@pytest.fixture
def points_data() -> QgsVectorLayer:
    layer = QgsVectorLayer(data_path("points.gpkg"), "points", "ogr")

    assert layer
    assert layer.isValid()

    return layer

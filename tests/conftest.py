import pytest
from pathlib import Path

from qgis.core import QgsRasterLayer, QgsProcessingFeedback, QgsProcessingContext


def data_path(file_name: str) -> str:

    path = Path(__file__).parent / "_data" / file_name

    return path.as_posix()


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

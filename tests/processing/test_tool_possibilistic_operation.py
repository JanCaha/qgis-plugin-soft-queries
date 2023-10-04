from pathlib import Path

from qgis.core import QgsRasterLayer

from soft_queries.processing.tool_possibilistic_operation import (
    PossibilisticOperationAlgorithm,
)

path_folder = Path(__file__).parent.parent / "_data"

path_r_1_poss = path_folder / "r_1_poss.tif"
path_r_1_nec = path_folder / "r_1_nec.tif"
path_r_2_poss = path_folder / "r_2_poss.tif"
path_r_2_nec = path_folder / "r_2_nec.tif"


def test_run(context, feedback):

    alg = PossibilisticOperationAlgorithm()
    alg.initAlgorithm()

    params = {
        "POSSIBILISTIC_RASTER_1": f"{path_r_1_poss.as_posix()}::~::{path_r_1_nec.as_posix()}",
        "POSSIBILISTIC_RASTER_2": f"{path_r_2_poss.as_posix()}::~::{path_r_2_nec.as_posix()}",
        "OPERATION": 0,
        "OPERATION_TYPE": 0,
        "OUTPUT_POSSIBILITY": "TEMPORARY_OUTPUT",
        "OUTPUT_NECESSITY": "TEMPORARY_OUTPUT",
    }

    alg.checkParameterValues(parameters=params, context=context)

    result = alg.run(parameters=params, context=context, feedback=feedback)

    assert result[1]
    assert isinstance(result[0], dict)

    assert isinstance(result[0]["OUTPUT_POSSIBILITY"], str)
    assert isinstance(QgsRasterLayer(result[0]["OUTPUT_POSSIBILITY"]), QgsRasterLayer)

    assert isinstance(result[0]["OUTPUT_NECESSITY"], str)
    assert isinstance(QgsRasterLayer(result[0]["OUTPUT_NECESSITY"]), QgsRasterLayer)

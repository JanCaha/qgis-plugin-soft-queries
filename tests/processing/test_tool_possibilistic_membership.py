from qgis.core import QgsRasterLayer

from soft_queries.processing.tool_possibilistic_membership import (
    PossibilisticMembershipAlgorithm,
)


def test_run(raster_layer_path: str, context, feedback):

    alg = PossibilisticMembershipAlgorithm()
    alg.initAlgorithm()

    params = {
        "FUZZY_NUMBER": "triangular;1005.0|1015.0|1025.0",
        "RASTER": raster_layer_path,
        "OUTPUT_POSSIBILITY": "TEMPORARY_OUTPUT",
        "OUTPUT_NECESSITY": "TEMPORARY_OUTPUT",
        "OPERATION": 0,
    }

    alg.checkParameterValues(parameters=params, context=context)

    result = alg.run(parameters=params, context=context, feedback=feedback)

    assert result[1]
    assert isinstance(result[0], dict)

    assert isinstance(result[0]["OUTPUT_POSSIBILITY"], str)
    assert isinstance(QgsRasterLayer(result[0]["OUTPUT_POSSIBILITY"]), QgsRasterLayer)

    assert isinstance(result[0]["OUTPUT_NECESSITY"], str)
    assert isinstance(QgsRasterLayer(result[0]["OUTPUT_NECESSITY"]), QgsRasterLayer)

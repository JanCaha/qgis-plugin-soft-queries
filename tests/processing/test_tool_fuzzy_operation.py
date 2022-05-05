from qgis.core import QgsRasterLayer

from soft_queries.processing.tool_fuzzy_operation import FuzzyOperationAlgorithm


def test_run(raster_fuzzy_1_path: str, raster_fuzzy_2_path: str, context, feedback):

    assert 1 == 1

    alg = FuzzyOperationAlgorithm()
    alg.initAlgorithm()

    params = {
        "FUZZY_RASTER_1": raster_fuzzy_1_path,
        "FUZZY_RASTER_2": raster_fuzzy_2_path,
        "OPERATION": 0,
        "OPERATION_TYPE": 0,
        "OUTPUT_FUZZY_MEMBERSHIP": "TEMPORARY_OUTPUT"
    }

    alg.checkParameterValues(parameters=params, context=context)

    result = alg.run(parameters=params, context=context, feedback=feedback)

    assert result[1]
    assert isinstance(result[0], dict)
    assert isinstance(result[0]["OUTPUT_FUZZY_MEMBERSHIP"], str)
    assert isinstance(QgsRasterLayer(result[0]["OUTPUT_FUZZY_MEMBERSHIP"]), QgsRasterLayer)


def test_to_avoid_crash():

    assert 0 == 1 - 1

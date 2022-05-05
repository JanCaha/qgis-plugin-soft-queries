from qgis.core import QgsRasterLayer

from soft_queries.processing.tool_fuzzy_membership import FuzzyMembershipAlgorithm


def test_run(raster_layer_path: str, context, feedback):

    alg = FuzzyMembershipAlgorithm()
    alg.initAlgorithm()

    params = {
        "FUZZY_NUMBER": "triangular;1005.0|1015.0|1025.0",
        "RASTER": raster_layer_path,
        "OUTPUT_FUZZY_MEMBERSHIP": "TEMPORARY_OUTPUT"
    }

    alg.checkParameterValues(parameters=params, context=context)

    result = alg.run(parameters=params, context=context, feedback=feedback)

    assert result[1]
    assert isinstance(result[0], dict)
    assert isinstance(result[0]["OUTPUT_FUZZY_MEMBERSHIP"], str)
    assert isinstance(QgsRasterLayer(result[0]["OUTPUT_FUZZY_MEMBERSHIP"]), QgsRasterLayer)

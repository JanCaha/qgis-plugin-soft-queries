from pathlib import Path

from qgis.core import QgsProcessingContext, QgsProcessingFeedback, QgsRasterLayer

from soft_queries.processing.tool_fuzzy_membership import FuzzyMembershipAlgorithm

input_raster_path = Path(__file__).parent / "dsm_epsg_5514.tif"

alg = FuzzyMembershipAlgorithm()
alg.initAlgorithm()

params = {
    "FUZZY_NUMBER": "triangular;1005.0|1015.0|1025.0",
    "RASTER": input_raster_path.as_posix(),
    "OUTPUT_FUZZY_MEMBERSHIP": "TEMPORARY_OUTPUT"
}

output_path = Path(__file__).parent / "fuzzy_1.tif"

params.update({"OUTPUT_FUZZY_MEMBERSHIP": output_path.as_posix()})

result = alg.run(parameters=params,
                 context=QgsProcessingContext(),
                 feedback=QgsProcessingFeedback())

output_path = Path(__file__).parent / "fuzzy_2.tif"

params.update({
    "FUZZY_NUMBER": "triangular;995.0|1005.0|1015.0",
    "OUTPUT_FUZZY_MEMBERSHIP": output_path.as_posix()
})

result = alg.run(parameters=params,
                 context=QgsProcessingContext(),
                 feedback=QgsProcessingFeedback())

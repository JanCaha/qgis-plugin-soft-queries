from pathlib import Path

from qgis.core import QgsProcessingContext, QgsProcessingFeedback

from soft_queries.processing.tool_fuzzy_membership import FuzzyMembershipAlgorithm
from soft_queries.processing.tool_possibilistic_membership import (
    PossibilisticMembershipAlgorithm,
)

input_raster_path = Path(__file__).parent / "dsm_epsg_5514.tif"


def fuzzy_rasters():

    alg = FuzzyMembershipAlgorithm()
    alg.initAlgorithm()

    params = {
        "FUZZY_NUMBER": "triangular;1005.0|1015.0|1025.0",
        "RASTER": input_raster_path.as_posix(),
        "OUTPUT_FUZZY_MEMBERSHIP": "TEMPORARY_OUTPUT",
    }

    output_path = Path(__file__).parent / "fuzzy_1.tif"

    params.update({"OUTPUT_FUZZY_MEMBERSHIP": output_path.as_posix()})

    result = alg.run(
        parameters=params,
        context=QgsProcessingContext(),
        feedback=QgsProcessingFeedback(),
    )

    output_path = Path(__file__).parent / "fuzzy_2.tif"

    params.update(
        {
            "FUZZY_NUMBER": "triangular;995.0|1005.0|1015.0",
            "OUTPUT_FUZZY_MEMBERSHIP": output_path.as_posix(),
        }
    )

    alg.run(
        parameters=params,
        context=QgsProcessingContext(),
        feedback=QgsProcessingFeedback(),
    )


def possibilistic_rasters():

    alg = PossibilisticMembershipAlgorithm()
    alg.initAlgorithm()

    output_path_poss = Path(__file__).parent / "r_1_poss.tif"
    output_path_nec = Path(__file__).parent / "r_1_nec.tif"

    params = {
        "FUZZY_NUMBER": "triangular;1005.0|1015.0|1025.0",
        "RASTER": input_raster_path.as_posix(),
        "OUTPUT_POSSIBILITY": output_path_poss.as_posix(),
        "OUTPUT_NECESSITY": output_path_nec.as_posix(),
        "OPERATION": 0,
    }

    alg.run(
        parameters=params,
        context=QgsProcessingContext(),
        feedback=QgsProcessingFeedback(),
    )

    output_path_poss = Path(__file__).parent / "r_2_poss.tif"
    output_path_nec = Path(__file__).parent / "r_2_nec.tif"

    params = {
        "FUZZY_NUMBER": "triangular;995.0|1005.0|1015.0",
        "RASTER": input_raster_path.as_posix(),
        "OUTPUT_POSSIBILITY": output_path_poss.as_posix(),
        "OUTPUT_NECESSITY": output_path_nec.as_posix(),
        "OPERATION": 0,
    }

    alg.run(
        parameters=params,
        context=QgsProcessingContext(),
        feedback=QgsProcessingFeedback(),
    )


if __name__ == "__main__":

    fuzzy_rasters()
    possibilistic_rasters()

from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingFeedback,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from .parameter_fuzzy_number import ParameterFuzzyNumber
from .utils import (
    RasterPart,
    create_raster,
    create_raster_writer,
    verify_one_band,
    writeBlock,
)


class FuzzyMembershipAlgorithm(QgsProcessingAlgorithm):

    FUZZYNUMBER = "FUZZY_NUMBER"
    RASTER = "RASTER"
    OUTPUT_FUZZY_MEMBERSHIP = "OUTPUT_FUZZY_MEMBERSHIP"

    def name(self):
        return "fuzzymembership"

    def displayName(self):
        return "Fuzzy Membership"

    def createInstance(self):
        return FuzzyMembershipAlgorithm()

    def initAlgorithm(self, config=None):

        self.addParameter(ParameterFuzzyNumber(self.FUZZYNUMBER, "Fuzzy Number"))

        self.addParameter(
            QgsProcessingParameterRasterLayer(self.RASTER, "Raster layer")
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_FUZZY_MEMBERSHIP, "Output raster layer - fuzzy membership"
            )
        )

    def checkParameterValues(self, parameters, context):

        input_raster = self.parameterAsRasterLayer(parameters, self.RASTER, context)

        rasters = [input_raster]

        if not verify_one_band(rasters):

            msg = "Input raster can have only one band."

            return False, msg

        return super().checkParameterValues(parameters, context)

    def processAlgorithm(self, parameters, context, feedback: QgsProcessingFeedback):

        raster_band = 1

        fuzzy_number = ParameterFuzzyNumber.valueToFuzzyNumber(
            parameters[self.FUZZYNUMBER]
        )

        input_raster = self.parameterAsRasterLayer(parameters, self.RASTER, context)

        input_raster_dp = input_raster.dataProvider()

        input_raster_nodata = input_raster_dp.sourceNoDataValue(raster_band)

        path_fuzzy_raster = self.parameterAsOutputLayer(
            parameters, self.OUTPUT_FUZZY_MEMBERSHIP, context
        )

        fuzzy_raster_writer = create_raster_writer(path_fuzzy_raster)

        fuzzy_raster_dp = create_raster(fuzzy_raster_writer, input_raster)

        if not fuzzy_raster_dp:
            raise QgsProcessingException("Data provider for fuzzy raster not created.")

        if not fuzzy_raster_dp.isValid():
            raise QgsProcessingException("Data provider for fuzzy raster not valid.")

        fuzzy_raster_dp.setNoDataValue(raster_band, input_raster_nodata)

        total = 100.0 / (input_raster.height()) if input_raster.height() else 0

        r_input_data = RasterPart(input_raster, raster_band)

        new_block = r_input_data.create_empty_block()

        count = 0

        while r_input_data.correct:

            if feedback.isCanceled():
                break

            for i in range(r_input_data.data_range):

                if r_input_data.isNoData(i):

                    new_block.setIsNoData(i)

                else:

                    new_block.setValue(
                        i, fuzzy_number.membership(r_input_data.value(i)).membership
                    )

            writeBlock(fuzzy_raster_dp, new_block, r_input_data)

            r_input_data.nextData()

            if r_input_data.correct:

                new_block = r_input_data.create_empty_block()

            feedback.setProgress(int(count * total))

            count += 1

        return {self.OUTPUT_FUZZY_MEMBERSHIP: path_fuzzy_raster}

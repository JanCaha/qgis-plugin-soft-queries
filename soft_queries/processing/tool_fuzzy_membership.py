from qgis.core import (QgsProcessingAlgorithm, QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterRasterLayer, QgsProcessingException,
                       QgsProcessingFeedback)

from .parameter_fuzzy_number import ParameterFuzzyNumber
from .utils import (create_raster_writer, create_raster, verify_one_band, create_raster_iterator,
                    create_empty_block)


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

        self.addParameter(QgsProcessingParameterRasterLayer(self.RASTER, "Raster layer"))

        self.addParameter(
            QgsProcessingParameterRasterDestination(self.OUTPUT_FUZZY_MEMBERSHIP,
                                                    "Output raster layer - fuzzy membership"))

    def checkParameterValues(self, parameters, context):

        input_raster = self.parameterAsRasterLayer(parameters, self.RASTER, context)

        rasters = [input_raster]

        if not verify_one_band(rasters):

            msg = "Input raster can have only one band."

            return False, msg

        return super().checkParameterValues(parameters, context)

    def processAlgorithm(self, parameters, context, feedback: QgsProcessingFeedback):

        raster_band = 1

        fuzzy_number = ParameterFuzzyNumber.valueToFuzzyNumber(parameters[self.FUZZYNUMBER])

        input_raster = self.parameterAsRasterLayer(parameters, self.RASTER, context)

        input_raster_dp = input_raster.dataProvider()

        input_raster_nodata = input_raster_dp.sourceNoDataValue(raster_band)

        path_fuzzy_raster = self.parameterAsOutputLayer(parameters, self.OUTPUT_FUZZY_MEMBERSHIP,
                                                        context)

        fuzzy_raster_writer = create_raster_writer(path_fuzzy_raster)

        fuzzy_raster_dp = create_raster(fuzzy_raster_writer, input_raster)

        if not fuzzy_raster_dp:
            raise QgsProcessingException("Data provider for fuzzy raster not created.")

        if not fuzzy_raster_dp.isValid():
            raise QgsProcessingException("Data provider for fuzzy raster not valid.")

        fuzzy_raster_dp.setNoDataValue(raster_band, input_raster_nodata)

        raster_iter = create_raster_iterator(input_raster, raster_band)

        total = 100.0 / (input_raster.height()) if input_raster.height() else 0

        success, nCols, nRows, input_data_block, topLeftCol, topLeftRow = raster_iter.readNextRasterPart(
            raster_band)

        new_block = create_empty_block(input_data_block)

        count = 0

        while (success):

            if feedback.isCanceled():
                break

            for i in range(input_data_block.height() * input_data_block.width()):

                if input_data_block.isNoData(i):

                    new_block.setIsNoData(i)

                else:

                    new_block.setValue(
                        i,
                        fuzzy_number.membership(input_data_block.value(i)).membership)

            fuzzy_raster_dp.writeBlock(new_block, raster_band, topLeftCol, topLeftRow)

            success, nCols, nRows, input_data_block, topLeftCol, topLeftRow = raster_iter.readNextRasterPart(
                raster_band)

            if success:

                new_block = create_empty_block(input_data_block)

            feedback.setProgress(int(count * total))

            count += 1

        return {self.OUTPUT_FUZZY_MEMBERSHIP: path_fuzzy_raster}

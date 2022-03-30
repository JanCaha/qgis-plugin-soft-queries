from qgis.core import (QgsProcessingAlgorithm, QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterRasterLayer, QgsProcessingException,
                       QgsProcessingFeedback)

from .parameter_fuzzy_number import ParameterFuzzyNumber
from .utils import (create_raster_writer, create_raster, verify_one_band, feedback_total)


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

        fuzzy_number = ParameterFuzzyNumber.valueToFuzzyNumber(parameters[self.FUZZYNUMBER])

        input_raster = self.parameterAsRasterLayer(parameters, self.RASTER, context)

        input_raster_dp = input_raster.dataProvider()

        path_fuzzy_raster = self.parameterAsOutputLayer(parameters, self.OUTPUT_FUZZY_MEMBERSHIP,
                                                        context)

        fuzzy_raster_writer = create_raster_writer(path_fuzzy_raster)

        fuzzy_raster_dp = create_raster(fuzzy_raster_writer, input_raster)

        if not fuzzy_raster_dp:
            raise QgsProcessingException("Data provider for fuzzy raster not created.")

        if not fuzzy_raster_dp.isValid():
            raise QgsProcessingException("Data provider for fuzzy raster not valid.")

        fuzzy_raster_dp.setNoDataValue(1, input_raster_dp.sourceNoDataValue(1))

        src_data = input_raster_dp.block(1, input_raster_dp.extent(), input_raster.width(),
                                         input_raster.height())

        fuzzy_data = fuzzy_raster_dp.block(1, input_raster_dp.extent(), input_raster.width(),
                                           input_raster.height())

        total = feedback_total(src_data)

        for i in range(src_data.height() * src_data.width()):

            if src_data.isNoData(i):

                fuzzy_data.setIsNoData(i)

            else:

                fuzzy_data.setValue(i, fuzzy_number.membership(src_data.value(i)).membership)

            feedback.setProgress(int(i * total))

        fuzzy_raster_dp.writeBlock(fuzzy_data, 1, 0, 0)

        return {self.OUTPUT_FUZZY_MEMBERSHIP: path_fuzzy_raster}

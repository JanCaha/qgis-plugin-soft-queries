from qgis.core import (QgsProcessingAlgorithm, QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterRasterLayer, QgsProcessingException,
                       QgsProcessingFeedback, QgsProcessingParameterEnum)

from ..FuzzyMath import (FuzzyNumberFactory, exceedance, undervaluation)

from .parameter_fuzzy_number import ParameterFuzzyNumber
from .utils import (create_raster_writer, create_raster, feedback_total, verify_one_band)


class PossibilisticMembershipAlgorithm(QgsProcessingAlgorithm):

    FUZZYNUMBER = "FUZZY_NUMBER"
    RASTER = "RASTER"
    OUTPUT_POSSIBILITY = "OUTPUT_POSSIBILITY"
    OUTPUT_NECESSITY = "OUTPUT_NECESSITY"
    OPERATION = "OPERATION"

    operation_enum = [
        "Raster values exceeds Fuzzy Number",
        "Raster values undervaluates Fuzzy Number",
    ]

    functions_operation_enum = [
        undervaluation,
        exceedance,
    ]

    def name(self):
        return "possibilisticmembership"

    def displayName(self):
        return "Possibilistic Membership"

    def createInstance(self):
        return PossibilisticMembershipAlgorithm()

    def initAlgorithm(self, config=None):

        self.addParameter(ParameterFuzzyNumber(self.FUZZYNUMBER, "Fuzzy Number"))

        self.addParameter(QgsProcessingParameterRasterLayer(self.RASTER, "Raster layer"))

        self.addParameter(
            QgsProcessingParameterEnum(self.OPERATION,
                                       "Operation to use",
                                       self.operation_enum,
                                       defaultValue=0))

        self.addParameter(
            QgsProcessingParameterRasterDestination(self.OUTPUT_POSSIBILITY,
                                                    "Output raster layer - possibility"))

        self.addParameter(
            QgsProcessingParameterRasterDestination(self.OUTPUT_NECESSITY,
                                                    "Output raster layer - necessity"))

    def checkParameterValues(self, parameters, context):

        input_raster = self.parameterAsRasterLayer(parameters, self.RASTER, context)

        rasters = [input_raster]

        if not verify_one_band(rasters):

            msg = "Input raster can have only one band."

            return False, msg

        return super().checkParameterValues(parameters, context)

    def processAlgorithm(self, parameters, context, feedback: QgsProcessingFeedback):

        fuzzy_number = ParameterFuzzyNumber.valueToFuzzyNumber(parameters[self.FUZZYNUMBER])

        operation_type = self.parameterAsEnum(parameters, self.OPERATION, context)

        operation_function = self.functions_operation_enum[operation_type]

        input_raster = self.parameterAsRasterLayer(parameters, self.RASTER, context)

        input_raster_dp = input_raster.dataProvider()

        path_possibility_raster = self.parameterAsOutputLayer(parameters, self.OUTPUT_POSSIBILITY,
                                                              context)

        path_necessity_raster = self.parameterAsOutputLayer(parameters, self.OUTPUT_NECESSITY,
                                                            context)

        possibility_raster_writer = create_raster_writer(path_possibility_raster)

        possibility_raster_dp = create_raster(possibility_raster_writer, input_raster)

        if not possibility_raster_dp:
            raise QgsProcessingException("Data provider for possibility not created.")

        if not possibility_raster_dp.isValid():
            raise QgsProcessingException("Data provider for possibility not valid.")

        necessity_raster_writer = create_raster_writer(path_necessity_raster)

        necessity_raster_dp = create_raster(necessity_raster_writer, input_raster)

        if not necessity_raster_dp:
            raise QgsProcessingException("Data provider for necessity not created.")

        if not necessity_raster_dp.isValid():
            raise QgsProcessingException("Data provider for necessity not valid.")

        possibility_raster_dp.setNoDataValue(1, input_raster_dp.sourceNoDataValue(1))
        necessity_raster_dp.setNoDataValue(1, input_raster_dp.sourceNoDataValue(1))

        src_data = input_raster_dp.block(1, input_raster_dp.extent(), input_raster.width(),
                                         input_raster.height())

        possibility_data = possibility_raster_dp.block(1, input_raster_dp.extent(),
                                                       input_raster.width(), input_raster.height())

        necessity_data = necessity_raster_dp.block(1, input_raster_dp.extent(),
                                                   input_raster.width(), input_raster.height())

        total = feedback_total(src_data)

        for i in range(src_data.height() * src_data.width()):

            if src_data.isNoData(i):

                possibility_data.setIsNoData(i)
                necessity_data.setIsNoData(i)

            else:

                pm = operation_function(fuzzy_number,
                                        FuzzyNumberFactory.crisp_number(src_data.value(i)))

                possibility_data.setValue(i, pm.possibility)
                necessity_data.setValue(i, pm.necessity)

            feedback.setProgress(int(i * total))

        possibility_raster_dp.writeBlock(possibility_data, 1, 0, 0)
        necessity_raster_dp.writeBlock(necessity_data, 1, 0, 0)

        return {
            self.OUTPUT_POSSIBILITY: path_possibility_raster,
            self.OUTPUT_NECESSITY: path_necessity_raster
        }

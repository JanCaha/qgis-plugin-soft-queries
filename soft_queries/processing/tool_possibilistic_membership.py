from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingFeedback,
    QgsProcessingParameterEnum,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from ..FuzzyMath import FuzzyNumberFactory, exceedance, undervaluation
from .parameter_fuzzy_number import ParameterFuzzyNumber
from .utils import (
    RasterPart,
    create_raster,
    create_raster_writer,
    verify_one_band,
    writeBlock,
)


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

        raster_band = 1

        fuzzy_number = ParameterFuzzyNumber.valueToFuzzyNumber(parameters[self.FUZZYNUMBER])

        operation_type = self.parameterAsEnum(parameters, self.OPERATION, context)

        operation_function = self.functions_operation_enum[operation_type]

        input_raster = self.parameterAsRasterLayer(parameters, self.RASTER, context)

        input_raster_dp = input_raster.dataProvider()

        input_raster_nodata = input_raster_dp.sourceNoDataValue(raster_band)

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

        possibility_raster_dp.setNoDataValue(raster_band, input_raster_nodata)
        necessity_raster_dp.setNoDataValue(raster_band, input_raster_nodata)

        total = 100.0 / (input_raster.height()) if input_raster.height() else 0

        r_input_data = RasterPart(input_raster, raster_band)

        new_block_possibility = r_input_data.create_empty_block()
        new_block_necessity = r_input_data.create_empty_block()

        count = 0

        while (r_input_data.correct):

            if feedback.isCanceled():
                break

            for i in range(r_input_data.data_range):

                if r_input_data.isNoData(i):

                    new_block_possibility.setIsNoData(i)
                    new_block_necessity.setIsNoData(i)

                else:

                    pm = operation_function(fuzzy_number,
                                            FuzzyNumberFactory.crisp_number(r_input_data.value(i)))

                    new_block_possibility.setValue(i, pm.possibility)
                    new_block_necessity.setValue(i, pm.necessity)

            writeBlock(possibility_raster_dp, new_block_possibility, r_input_data)
            writeBlock(necessity_raster_dp, new_block_necessity, r_input_data)

            r_input_data.nextData()

            if r_input_data.correct:

                new_block_possibility = r_input_data.create_empty_block()
                new_block_necessity = r_input_data.create_empty_block()

            feedback.setProgress(int(count * total))

            count += 1

        return {
            self.OUTPUT_POSSIBILITY: path_possibility_raster,
            self.OUTPUT_NECESSITY: path_necessity_raster
        }

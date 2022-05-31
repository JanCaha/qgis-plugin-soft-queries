from qgis.core import (QgsProcessingAlgorithm, QgsProcessingParameterRasterDestination,
                       QgsProcessingException, QgsProcessingFeedback, QgsProcessingParameterEnum)

from ..FuzzyMath.class_membership_operations import PossibilisticAnd, PossibilisticOr, PossibilisticMembership

from .utils import (create_raster_writer, create_raster, verify_crs_equal, verify_extent_equal,
                    verify_size_equal, verify_one_band, RasterPart, writeBlock)

from .parameter_possibilistic_element import ParameterPossibilisticElement


class PossibilisticOperationAlgorithm(QgsProcessingAlgorithm):

    POSSIBILISTIC_RASTER_1 = "POSSIBILISTIC_RASTER_1"
    POSSIBILISTIC_RASTER_2 = "POSSIBILISTIC_RASTER_2"
    OPERATION = "OPERATION"
    OPERATION_TYPE = "OPERATION_TYPE"

    OUTPUT_POSSIBILITY = "OUTPUT_POSSIBILITY"
    OUTPUT_NECESSITY = "OUTPUT_NECESSITY"

    operations_enum = ["And", "Or"]

    operations = {"And": PossibilisticAnd.possibilisticAnd, "Or": PossibilisticOr.possibilisticOr}

    operations_types_enum = [
        "min/max", "product", "drastic", "Lukasiewicz", "Nilpotent", "Hamacher"
    ]

    def name(self):
        return "possibilisticoperation"

    def displayName(self):
        return "Possibilistic Operation"

    def createInstance(self):
        return PossibilisticOperationAlgorithm()

    def initAlgorithm(self, config=None):

        self.addParameter(
            ParameterPossibilisticElement(self.POSSIBILISTIC_RASTER_1, "Possibilistic Layer 1"))

        self.addParameter(
            ParameterPossibilisticElement(self.POSSIBILISTIC_RASTER_2, "Possibilistic Layer 2"))

        self.addParameter(
            QgsProcessingParameterEnum(self.OPERATION,
                                       "Operation to use",
                                       self.operations_enum,
                                       defaultValue=self.operations_enum[0]))

        self.addParameter(
            QgsProcessingParameterEnum(self.OPERATION_TYPE,
                                       "Operation type",
                                       self.operations_types_enum,
                                       defaultValue=self.operations_types_enum[0]))

        self.addParameter(
            QgsProcessingParameterRasterDestination(self.OUTPUT_POSSIBILITY,
                                                    "Output raster layer - possibility"))

        self.addParameter(
            QgsProcessingParameterRasterDestination(self.OUTPUT_NECESSITY,
                                                    "Output raster layer - necessity"))

    def checkParameterValues(self, parameters, context):

        raster_1_possibility, raster_1_necessity = ParameterPossibilisticElement.valueToRasters(
            parameters[self.POSSIBILISTIC_RASTER_1])

        raster_2_possibility, raster_2_necessity = ParameterPossibilisticElement.valueToRasters(
            parameters[self.POSSIBILISTIC_RASTER_2])

        rasters = [
            raster_1_possibility, raster_1_necessity, raster_2_possibility, raster_2_necessity
        ]

        if not verify_one_band(rasters):

            msg = "Input rasters can have only one band. One of them has other band number."

            return False, msg

        if not verify_crs_equal(rasters):

            msg = "CRS of input rasters have to be equal. Right now they are not."

            return False, msg

        if not verify_size_equal(rasters):

            msg = "Sizes of input rasters have to be equal. Right now they are not."

            return False, msg

        if not verify_extent_equal(rasters):

            msg = "Extents of input rasters have to be equal. Right now they are not."

            return False, msg

        return super().checkParameterValues(parameters, context)

    def processAlgorithm(self, parameters, context, feedback: QgsProcessingFeedback):

        raster_band = 1

        raster_1_possibility, raster_1_necessity = ParameterPossibilisticElement.valueToRasters(
            parameters[self.POSSIBILISTIC_RASTER_1])

        raster_2_possibility, raster_2_necessity = ParameterPossibilisticElement.valueToRasters(
            parameters[self.POSSIBILISTIC_RASTER_2])

        operation = self.parameterAsEnumString(parameters, self.OPERATION, context)
        operation = self.operations[operation]

        operation_type = self.parameterAsEnumString(parameters, self.OPERATION_TYPE, context)

        if "/" in operation_type:

            if operation == self.operations["And"]:
                operation_type = operation_type.split("/")[0]
            else:
                operation_type = operation_type.split("/")[1]

        feedback.pushInfo("Processing operation `{}` with type of operation `{}`.".format(
            operation.__name__, operation_type))

        raster_1_possibility_dp = raster_1_possibility.dataProvider()

        fuzzy_input_nodata = raster_1_possibility_dp.sourceNoDataValue(raster_band)

        path_possibility_raster = self.parameterAsOutputLayer(parameters, self.OUTPUT_POSSIBILITY,
                                                              context)

        path_necessity_raster = self.parameterAsOutputLayer(parameters, self.OUTPUT_NECESSITY,
                                                            context)

        possibility_raster_writer = create_raster_writer(path_possibility_raster)

        possibility_raster_dp = create_raster(possibility_raster_writer, raster_1_possibility)

        if not possibility_raster_dp:
            raise QgsProcessingException("Data provider for possibility not created.")

        if not possibility_raster_dp.isValid():
            raise QgsProcessingException("Data provider for possibility not valid.")

        necessity_raster_writer = create_raster_writer(path_necessity_raster)

        necessity_raster_dp = create_raster(necessity_raster_writer, raster_1_possibility)

        if not necessity_raster_dp:
            raise QgsProcessingException("Data provider for necessity not created.")

        if not necessity_raster_dp.isValid():
            raise QgsProcessingException("Data provider for necessity not valid.")

        possibility_raster_dp.setNoDataValue(raster_band, fuzzy_input_nodata)
        necessity_raster_dp.setNoDataValue(raster_band, fuzzy_input_nodata)

        total = 100.0 / (raster_1_possibility.height()) if raster_1_possibility.height() else 0

        r_1_poss_data = RasterPart(raster_1_possibility, raster_band)
        r_1_nec_data = RasterPart(raster_1_necessity, raster_band)

        r_2_poss_data = RasterPart(raster_2_possibility, raster_band)
        r_2_nec_data = RasterPart(raster_2_necessity, raster_band)

        possibility_new_block = r_1_poss_data.create_empty_block()
        necessity_new_block = r_1_poss_data.create_empty_block()

        count = 0

        while (r_1_poss_data.correct and r_1_nec_data.correct and r_2_poss_data.correct and
               r_2_nec_data.correct):

            if feedback.isCanceled():
                break

            for i in range(r_1_poss_data.data_range):

                if r_1_poss_data.isNoData(i) or\
                    r_1_nec_data.isNoData(i) or\
                    r_2_poss_data.isNoData(i) or\
                    r_2_poss_data.isNoData(i):

                    possibility_new_block.setIsNoData(i)
                    necessity_new_block.setIsNoData(i)

                else:

                    pm = operation(
                        PossibilisticMembership(r_1_poss_data.value(i), r_1_nec_data.value(i)),
                        PossibilisticMembership(r_2_poss_data.value(i), r_2_nec_data.value(i)),
                        operation_type)

                    possibility_new_block.setValue(i, pm.possibility)
                    necessity_new_block.setValue(i, pm.necessity)

            writeBlock(possibility_raster_dp, possibility_new_block, r_1_poss_data)
            writeBlock(necessity_raster_dp, necessity_new_block, r_1_poss_data)

            r_1_poss_data.nextData()
            r_1_nec_data.nextData()
            r_2_poss_data.nextData()
            r_2_nec_data.nextData()

            if (r_1_poss_data.correct and r_1_nec_data.correct and r_2_poss_data.correct and
                    r_2_nec_data.correct):

                possibility_new_block = r_1_poss_data.create_empty_block()
                necessity_new_block = r_1_poss_data.create_empty_block()

            feedback.setProgress(int(count * total))

            count += 1

        return {
            self.OUTPUT_POSSIBILITY: path_possibility_raster,
            self.OUTPUT_NECESSITY: path_necessity_raster
        }

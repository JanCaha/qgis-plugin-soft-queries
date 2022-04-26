from qgis.core import (QgsProcessingAlgorithm, QgsProcessingParameterRasterDestination,
                       QgsProcessingException, QgsProcessingFeedback, QgsProcessingParameterEnum)

from ..FuzzyMath.class_membership_operations import PossibilisticAnd, PossibilisticOr, PossibilisticMembership

from .utils import (create_raster_writer, create_raster, verify_crs_equal, verify_extent_equal,
                    verify_size_equal, verify_one_band, create_raster_iterator, create_empty_block)

from .parameter_possibilistic_element import ParameterPossibilisticElement


class PossibilisticOperationAlgorithm(QgsProcessingAlgorithm):

    POSSIBILISTIC_RASTER_1 = "POSSIBILISTIC_RASTER_1"
    POSSIBILISTIC_RASTER_2 = "POSSIBILISTIC_RASTER_2"
    OPERATION = "OPERATION"
    OPERATION_TYPE = "OPERATION_TYPE"

    OUTPUT_POSSIBILITY = "OUTPUT_POSSIBILITY"
    OUTPUT_NECESSITY = "OUTPUT_NECESSITY"

    operations_enum = ["And", "Or"]

    operations = [PossibilisticAnd.possibilisticAnd, PossibilisticOr.possibilisticOr]

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
                                       defaultValue=0))

        self.addParameter(
            QgsProcessingParameterEnum(self.OPERATION_TYPE,
                                       "Operation type",
                                       self.operations_types_enum,
                                       defaultValue=0))

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

        operation_index = self.parameterAsEnum(parameters, self.OPERATION, context)
        operation = self.operations[operation_index]

        operation_type_index = self.parameterAsEnum(parameters, self.OPERATION_TYPE, context)
        operation_type = self.operations_types_enum[operation_type_index]

        if "/" in operation_type:

            if operation_index == 0:
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

        raster_1_possibility_raster_iter = create_raster_iterator(raster_1_possibility,
                                                                  raster_band)
        raster_1_necessity_raster_iter = create_raster_iterator(raster_1_necessity, raster_band)
        raster_2_possibility_raster_iter = create_raster_iterator(raster_2_possibility,
                                                                  raster_band)
        raster_2_necessity_raster_iter = create_raster_iterator(raster_2_necessity, raster_band)

        success_1_poss, nCols, nRows, raster_1_possibility_data_block, topLeftCol, topLeftRow = raster_1_possibility_raster_iter.readNextRasterPart(
            raster_band)

        success_1_nec, nCols, nRows, raster_1_necessity_data_block, topLeftCol, topLeftRow = raster_1_necessity_raster_iter.readNextRasterPart(
            raster_band)

        success_2_poss, nCols, nRows, raster_2_possibility_data_block, topLeftCol, topLeftRow = raster_2_possibility_raster_iter.readNextRasterPart(
            raster_band)

        success_2_nec, nCols, nRows, raster_2_necessity_data_block, topLeftCol, topLeftRow = raster_2_necessity_raster_iter.readNextRasterPart(
            raster_band)

        possibility_new_block = create_empty_block(raster_1_possibility_data_block)
        necessity_new_block = create_empty_block(raster_1_possibility_data_block)

        count = 0

        while (success_1_poss and success_1_nec and success_2_poss and success_2_nec):

            if feedback.isCanceled():
                break

            for i in range(raster_1_possibility_data_block.height() *
                           raster_1_possibility_data_block.width()):

                if raster_1_possibility_data_block.isNoData(i) or\
                    raster_1_necessity_data_block.isNoData(i) or\
                    raster_2_possibility_data_block.isNoData(i) or\
                    raster_2_necessity_data_block.isNoData(i):

                    possibility_new_block.setIsNoData(i)
                    necessity_new_block.setIsNoData(i)

                else:

                    pm = operation(
                        PossibilisticMembership(raster_1_possibility_data_block.value(i),
                                                raster_1_necessity_data_block.value(i)),
                        PossibilisticMembership(raster_2_possibility_data_block.value(i),
                                                raster_2_necessity_data_block.value(i)),
                        operation_type)

                    possibility_new_block.setValue(i, pm.possibility)
                    necessity_new_block.setValue(i, pm.necessity)

            possibility_raster_dp.writeBlock(possibility_new_block, raster_band, topLeftCol,
                                             topLeftRow)
            necessity_raster_dp.writeBlock(necessity_new_block, raster_band, topLeftCol,
                                           topLeftRow)

            success_1_poss, nCols, nRows, raster_1_possibility_data_block, topLeftCol, topLeftRow = raster_1_possibility_raster_iter.readNextRasterPart(
                raster_band)

            success_1_nec, nCols, nRows, raster_1_necessity_data_block, topLeftCol, topLeftRow = raster_1_necessity_raster_iter.readNextRasterPart(
                raster_band)

            success_2_poss, nCols, nRows, raster_2_possibility_data_block, topLeftCol, topLeftRow = raster_2_possibility_raster_iter.readNextRasterPart(
                raster_band)

            success_2_nec, nCols, nRows, raster_2_necessity_data_block, topLeftCol, topLeftRow = raster_2_necessity_raster_iter.readNextRasterPart(
                raster_band)

            if (success_1_poss and success_1_nec and success_2_poss and success_2_nec):

                possibility_new_block = create_empty_block(raster_1_possibility_data_block)
                necessity_new_block = create_empty_block(raster_1_possibility_data_block)

            feedback.setProgress(int(count * total))

            count += 1

        return {
            self.OUTPUT_POSSIBILITY: path_possibility_raster,
            self.OUTPUT_NECESSITY: path_necessity_raster
        }

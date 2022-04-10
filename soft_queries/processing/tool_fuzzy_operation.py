from qgis.core import (QgsProcessingAlgorithm, QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterRasterLayer, QgsProcessingException,
                       QgsProcessingFeedback, QgsProcessingParameterEnum)

from ..FuzzyMath.class_membership_operations import FuzzyAnd, FuzzyOr, FuzzyMembership

from .utils import (create_raster_writer, create_raster, verify_crs_equal, verify_extent_equal,
                    verify_size_equal, verify_one_band, create_raster_iterator, create_empty_block)


class FuzzyOperationAlgorithm(QgsProcessingAlgorithm):

    FUZZY_RASTER_1 = "FUZZY_RASTER_1"
    FUZZY_RASTER_2 = "FUZZY_RASTER_2"
    OPERATION = "OPERATION"
    OPERATION_TYPE = "OPERATION_TYPE"

    OUTPUT_FUZZY_MEMBERSHIP = "OUTPUT_FUZZY_MEMBERSHIP"

    operations_enum = ["And", "Or"]

    operations = [FuzzyAnd.fuzzyAnd, FuzzyOr.fuzzyOr]

    operations_types_enum = [
        "min/max", "product", "drastic", "Lukasiewicz", "Nilpotent", "Hamacher"
    ]

    def name(self):
        return "fuzzyoperation"

    def displayName(self):
        return "Fuzzy Operation"

    def createInstance(self):
        return FuzzyOperationAlgorithm()

    def initAlgorithm(self, config=None):

        self.addParameter(QgsProcessingParameterRasterLayer(self.FUZZY_RASTER_1, "Raster Layer 1"))

        self.addParameter(QgsProcessingParameterRasterLayer(self.FUZZY_RASTER_2, "Raster Layer 2"))

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
            QgsProcessingParameterRasterDestination(self.OUTPUT_FUZZY_MEMBERSHIP,
                                                    "Output raster layer - fuzzy membership"))

    def checkParameterValues(self, parameters, context):

        fuzzy_input_raster_1 = self.parameterAsRasterLayer(parameters, self.FUZZY_RASTER_1,
                                                           context)
        fuzzy_input_raster_2 = self.parameterAsRasterLayer(parameters, self.FUZZY_RASTER_2,
                                                           context)

        rasters = [fuzzy_input_raster_1, fuzzy_input_raster_2]

        if not verify_one_band(rasters):

            msg = "Input rasters can have only one band. One of them has other band number."

            return False, msg

        if not verify_crs_equal(rasters):

            msg = "CRS of input rasters have to be equal. Right now they are not." \
                  "{} = {}".format(fuzzy_input_raster_1.crs().authid(), fuzzy_input_raster_2.crs().authid())

            return False, msg

        if not verify_size_equal(rasters):

            msg = "Sizes of input rasters have to be equal. Right now they are not " \
                  "({}, {}) = ({}, {})".format(fuzzy_input_raster_1.height(), fuzzy_input_raster_1.width(),
                                               fuzzy_input_raster_2.height(), fuzzy_input_raster_2.width())

            return False, msg

        if not verify_extent_equal(rasters):

            msg = "Extents of input rasters have to be equal. Right now they are not."

            return False, msg

        return super().checkParameterValues(parameters, context)

    def processAlgorithm(self, parameters, context, feedback: QgsProcessingFeedback):

        raster_band = 1

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

        fuzzy_input_raster_1 = self.parameterAsRasterLayer(parameters, self.FUZZY_RASTER_1,
                                                           context)
        fuzzy_input_raster_2 = self.parameterAsRasterLayer(parameters, self.FUZZY_RASTER_2,
                                                           context)

        fuzzy_input_raster_1_dp = fuzzy_input_raster_1.dataProvider()

        fuzzy_input_nodata = fuzzy_input_raster_1_dp.sourceNoDataValue(raster_band)

        path_fuzzy_raster = self.parameterAsOutputLayer(parameters, self.OUTPUT_FUZZY_MEMBERSHIP,
                                                        context)

        output_fuzzy_raster_writer = create_raster_writer(path_fuzzy_raster)

        output_fuzzy_raster_dp = create_raster(output_fuzzy_raster_writer, fuzzy_input_raster_1)

        if not output_fuzzy_raster_dp:
            raise QgsProcessingException("Data provider for fuzzy raster not created.")

        if not output_fuzzy_raster_dp.isValid():
            raise QgsProcessingException("Data provider for fuzzy raster not valid.")

        output_fuzzy_raster_dp.setNoDataValue(raster_band, fuzzy_input_nodata)

        fuzzy_1_raster_iter = create_raster_iterator(fuzzy_input_raster_1, raster_band)
        fuzzy_2_raster_iter = create_raster_iterator(fuzzy_input_raster_2, raster_band)

        total = 100.0 / (fuzzy_input_raster_1.height()) if fuzzy_input_raster_1.height() else 0

        success_f_1, nCols, nRows, fuzzy_1_input_data_block, topLeftCol, topLeftRow = fuzzy_1_raster_iter.readNextRasterPart(
            raster_band)

        success_f_2, nCols, nRows, fuzzy_2_input_data_block, topLeftCol, topLeftRow = fuzzy_2_raster_iter.readNextRasterPart(
            raster_band)

        new_block = create_empty_block(fuzzy_1_input_data_block)

        count = 0

        while (success_f_1, success_f_2):

            if feedback.isCanceled():
                break

            for i in range(fuzzy_1_input_data_block.height() * fuzzy_1_input_data_block.width()):

                if fuzzy_1_input_data_block.isNoData(i) or fuzzy_2_input_data_block.setIsNoData(i):

                    new_block.setIsNoData(i)

                else:

                    fm = operation(FuzzyMembership(fuzzy_1_input_data_block.value(i)),
                                   FuzzyMembership(fuzzy_2_input_data_block.value(i)),
                                   operation_type)

                    new_block.setValue(i, fm.membership)

            output_fuzzy_raster_dp.writeBlock(new_block, raster_band, topLeftCol, topLeftRow)

            success_f_1, nCols, nRows, fuzzy_1_input_data_block, topLeftCol, topLeftRow = fuzzy_1_raster_iter.readNextRasterPart(
                raster_band)

            success_f_2, nCols, nRows, fuzzy_2_input_data_block, topLeftCol, topLeftRow = fuzzy_2_raster_iter.readNextRasterPart(
                raster_band)

            if (success_f_1 and success_f_2):

                new_block = create_empty_block(fuzzy_1_input_data_block)

            feedback.setProgress(int(count * total))

            count += 1

        return {self.OUTPUT_FUZZY_MEMBERSHIP: path_fuzzy_raster}

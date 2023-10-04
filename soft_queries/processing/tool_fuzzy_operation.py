from FuzzyMath.class_membership_operations import FuzzyAnd, FuzzyMembership, FuzzyOr
from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingFeedback,
    QgsProcessingParameterEnum,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterRasterLayer,
)

from .utils import (
    RasterPart,
    create_raster,
    create_raster_writer,
    verify_crs_equal,
    verify_extent_equal,
    verify_one_band,
    verify_size_equal,
    writeBlock,
)


class FuzzyOperationAlgorithm(QgsProcessingAlgorithm):
    FUZZY_RASTER_1 = "FUZZY_RASTER_1"
    FUZZY_RASTER_2 = "FUZZY_RASTER_2"
    OPERATION = "OPERATION"
    OPERATION_TYPE = "OPERATION_TYPE"

    OUTPUT_FUZZY_MEMBERSHIP = "OUTPUT_FUZZY_MEMBERSHIP"

    operations_enum = ["And", "Or"]

    operations = {"And": FuzzyAnd.fuzzyAnd, "Or": FuzzyOr.fuzzyOr}

    operations_types_enum = [
        "min/max",
        "product",
        "drastic",
        "Lukasiewicz",
        "Nilpotent",
        "Hamacher",
    ]

    def name(self):
        return "fuzzyoperation"

    def displayName(self):
        return "Fuzzy Operation"

    def createInstance(self):
        return FuzzyOperationAlgorithm()

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterRasterLayer(self.FUZZY_RASTER_1, "Raster Layer 1")
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(self.FUZZY_RASTER_2, "Raster Layer 2")
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                self.OPERATION,
                "Operation to use",
                self.operations_enum,
                defaultValue=self.operations_enum[0],
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                self.OPERATION_TYPE,
                "Operation type",
                self.operations_types_enum,
                defaultValue=self.operations_types_enum[0],
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_FUZZY_MEMBERSHIP, "Output raster layer - fuzzy membership"
            )
        )

    def checkParameterValues(self, parameters, context):
        fuzzy_input_raster_1 = self.parameterAsRasterLayer(
            parameters, self.FUZZY_RASTER_1, context
        )
        fuzzy_input_raster_2 = self.parameterAsRasterLayer(
            parameters, self.FUZZY_RASTER_2, context
        )

        rasters = [fuzzy_input_raster_1, fuzzy_input_raster_2]

        if not verify_one_band(rasters):
            msg = "Input rasters can have only one band. One of them has other band number."

            return False, msg

        if not verify_crs_equal(rasters):
            msg = (
                "CRS of input rasters have to be equal. Right now they are not."
                "{} = {}".format(
                    fuzzy_input_raster_1.crs().authid(),
                    fuzzy_input_raster_2.crs().authid(),
                )
            )

            return False, msg

        if not verify_size_equal(rasters):
            msg = (
                "Sizes of input rasters have to be equal. Right now they are not "
                "({}, {}) = ({}, {})".format(
                    fuzzy_input_raster_1.height(),
                    fuzzy_input_raster_1.width(),
                    fuzzy_input_raster_2.height(),
                    fuzzy_input_raster_2.width(),
                )
            )

            return False, msg

        if not verify_extent_equal(rasters):
            msg = "Extents of input rasters have to be equal. Right now they are not."

            return False, msg

        return super().checkParameterValues(parameters, context)

    def processAlgorithm(self, parameters, context, feedback: QgsProcessingFeedback):
        raster_band = 1

        fuzzy_operation = self.parameterAsEnumString(
            parameters, self.OPERATION, context
        )
        fuzzy_operation = self.operations[fuzzy_operation]

        operation_type = self.parameterAsEnumString(
            parameters, self.OPERATION_TYPE, context
        )

        if "/" in operation_type:
            if fuzzy_operation == self.operations["And"]:
                operation_type = operation_type.split("/")[0]
            else:
                operation_type = operation_type.split("/")[1]

        feedback.pushInfo(
            "Processing operation `{}` with type of operation `{}`.".format(
                fuzzy_operation.__name__, operation_type
            )
        )

        fuzzy_input_raster_1 = self.parameterAsRasterLayer(
            parameters, self.FUZZY_RASTER_1, context
        )
        fuzzy_input_raster_2 = self.parameterAsRasterLayer(
            parameters, self.FUZZY_RASTER_2, context
        )

        fuzzy_input_raster_1_dp = fuzzy_input_raster_1.dataProvider()

        fuzzy_input_nodata = fuzzy_input_raster_1_dp.sourceNoDataValue(raster_band)

        path_fuzzy_raster = self.parameterAsOutputLayer(
            parameters, self.OUTPUT_FUZZY_MEMBERSHIP, context
        )

        output_fuzzy_raster_writer = create_raster_writer(path_fuzzy_raster)

        output_fuzzy_raster_dp = create_raster(
            output_fuzzy_raster_writer, fuzzy_input_raster_1
        )

        if not output_fuzzy_raster_dp:
            raise QgsProcessingException("Data provider for fuzzy raster not created.")

        if not output_fuzzy_raster_dp.isValid():
            raise QgsProcessingException("Data provider for fuzzy raster not valid.")

        output_fuzzy_raster_dp.setNoDataValue(raster_band, fuzzy_input_nodata)

        total = (
            100.0 / (fuzzy_input_raster_1.height())
            if fuzzy_input_raster_1.height()
            else 0
        )

        r_fuzzy_1 = RasterPart(fuzzy_input_raster_1, raster_band)
        r_fuzzy_2 = RasterPart(fuzzy_input_raster_2, raster_band)

        new_block = r_fuzzy_1.create_empty_block()

        count = 0

        while r_fuzzy_1.correct and r_fuzzy_2.correct:
            if feedback.isCanceled():
                break

            for i in range(r_fuzzy_1.data_range):
                if r_fuzzy_1.isNoData(i) or r_fuzzy_2.isNoData(i):
                    new_block.setIsNoData(i)

                else:
                    fm = fuzzy_operation(
                        FuzzyMembership(r_fuzzy_1.value(i)),
                        FuzzyMembership(r_fuzzy_2.value(i)),
                        operation_type,
                    )

                    new_block.setValue(i, fm.membership)

            writeBlock(output_fuzzy_raster_dp, new_block, r_fuzzy_1)

            r_fuzzy_1.nextData()
            r_fuzzy_2.nextData()

            if r_fuzzy_1.correct and r_fuzzy_2.correct:
                new_block = r_fuzzy_1.create_empty_block()

            feedback.setProgress(int(count * total))

            count += 1

        return {self.OUTPUT_FUZZY_MEMBERSHIP: path_fuzzy_raster}

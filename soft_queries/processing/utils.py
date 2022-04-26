from typing import List
from pathlib import Path

from qgis.core import (QgsRasterFileWriter, QgsRasterLayer, QgsRasterDataProvider, Qgis,
                       QgsRasterBlock, QgsRasterIterator)


def create_raster_writer(path_raster: str) -> QgsRasterFileWriter:

    raster_writer = QgsRasterFileWriter(path_raster)

    raster_writer.setOutputProviderKey('gdal')

    ext = Path(path_raster).suffix.replace(".", "")

    driver = raster_writer.driverForExtension(ext)

    raster_writer.setOutputFormat(driver)

    return raster_writer


def create_raster(raster_writer: QgsRasterFileWriter,
                  template_raster: QgsRasterLayer) -> QgsRasterDataProvider:

    return raster_writer.createOneBandRaster(Qgis.Float64, template_raster.width(),
                                             template_raster.height(), template_raster.extent(),
                                             template_raster.crs())


def verify_crs_equal(rasters: List[QgsRasterLayer]) -> bool:

    crs_to_check = None

    for raster in rasters:

        if crs_to_check is None:
            crs_to_check = raster.crs()

        else:

            if crs_to_check.toWkt() != raster.crs().toWkt():
                return False

    return True


def verify_size_equal(rasters: List[QgsRasterLayer]) -> bool:

    size = None

    for raster in rasters:

        if size is None:
            size = [raster.width(), raster.height()]

        else:

            if size != [raster.width(), raster.height()]:
                return False

    return True


def verify_extent_equal(rasters: List[QgsRasterLayer]) -> bool:

    extent = None

    for raster in rasters:

        if extent is None:
            extent = raster.extent()

        else:

            if extent.asWktPolygon() != raster.extent().asWktPolygon():
                return False

    return True


def verify_one_band(rasters: List[QgsRasterLayer]) -> bool:

    for raster in rasters:

        if raster.bandCount() != 1:
            return False

    return True


def feedback_total(data_block: QgsRasterBlock):

    return 100.0 / (data_block.height() * data_block.width())\
        if data_block.height() and data_block.width() else 0


def create_raster_iterator(input_raster: QgsRasterLayer,
                           raster_band: int = 1) -> QgsRasterIterator:

    input_raster_dp = input_raster.dataProvider()

    raster_iter = QgsRasterIterator(input_raster_dp)

    raster_iter.startRasterRead(raster_band, input_raster_dp.xSize(), input_raster_dp.ySize(),
                                input_raster_dp.extent())

    raster_iter.setMaximumTileHeight(1)
    raster_iter.setMaximumTileHeight(1)

    return raster_iter


def create_empty_block(input_block: QgsRasterBlock) -> QgsRasterBlock:

    new_block = QgsRasterBlock(Qgis.Float64, input_block.width(), input_block.height())

    new_block.setNoDataValue(input_block.noDataValue())

    return new_block

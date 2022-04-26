from pathlib import Path

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import (QLabel, QGroupBox)
from qgis.gui import QgsMapLayerComboBox

from qgis.core import QgsRasterLayer, QgsMapLayerProxyModel

from processing.gui.wrappers import WidgetWrapper

path_file = Path(__file__)

path_widget_ui = path_file.parent / "widgetpossibilisticelement.ui"

WIDGET, BASE = uic.loadUiType(path_widget_ui.absolute())


class PossibilisticElementWidget(BASE, WIDGET):

    groupbox: QGroupBox

    label_possibility: QLabel
    label_necessity: QLabel

    maplayer_possibility: QgsMapLayerComboBox
    maplayer_necessity: QgsMapLayerComboBox

    raster_possibility: QgsRasterLayer
    raster_necessity: QgsRasterLayer

    text_separator: str = "::~::"

    def __init__(self, parent=None) -> None:

        super(PossibilisticElementWidget, self).__init__(None)

        self.setupUi(self)

        self.maplayer_possibility.setFilters(QgsMapLayerProxyModel.RasterLayer)
        self.maplayer_necessity.setFilters(QgsMapLayerProxyModel.RasterLayer)

        self.maplayer_possibility.layerChanged.connect(self.update_rasters)
        self.maplayer_necessity.layerChanged.connect(self.update_rasters)

        self.update_rasters()

    def update_rasters(self):
        self.raster_possibility = self.maplayer_possibility.currentLayer()
        self.raster_necessity = self.maplayer_necessity.currentLayer()

    def setValue(self, value: str):

        split_value = value.split(self.text_separator)

        self.raster_possibility = QgsRasterLayer(split_value[0])
        self.raster_necessity = QgsRasterLayer(split_value[1])

        self.maplayer_possibility.setLayer(self.raster_possibility)
        self.maplayer_necessity.setLayer(self.raster_necessity)

    def value(self):

        return "{}{}{}".format(self.raster_possibility.dataProvider().dataSourceUri(),
                               self.text_separator,
                               self.raster_necessity.dataProvider().dataSourceUri())

    def value_as_dict(self):

        return {
            "possibility": self.raster_possibility.dataProvider().dataSourceUri(),
            "necessity": self.raster_necessity.dataProvider().dataSourceUri()
        }


# https://github.com/qgis/QGIS/blob/master/python/plugins/processing/algs/qgis/ui/ReliefColorsWidget.py


class PossibilisticElementWidgetWrapper(WidgetWrapper):

    def createWidget(self):
        return PossibilisticElementWidget()

    def setValue(self, value):
        self.widget.setValue(value)

    def value(self):
        return self.widget.value()

from processing.gui.wrappers import WidgetWrapper
from qgis.core import QgsMapLayerProxyModel, QgsRasterLayer
from qgis.gui import QgsMapLayerComboBox
from qgis.PyQt.QtWidgets import QFormLayout, QGroupBox, QVBoxLayout, QWidget


class PossibilisticElementWidget(QWidget):

    groupbox: QGroupBox

    maplayer_possibility: QgsMapLayerComboBox
    maplayer_necessity: QgsMapLayerComboBox

    raster_possibility: QgsRasterLayer
    raster_necessity: QgsRasterLayer

    text_separator: str = "::~::"

    def __init__(self, parent=None) -> None:

        super(PossibilisticElementWidget, self).__init__(parent)

        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        self.groupbox = QGroupBox("Raster Definitions", self)
        main_layout.addWidget(self.groupbox)

        layout = QFormLayout(self)
        self.groupbox.setLayout(layout)

        self.maplayer_possibility = QgsMapLayerComboBox(self)
        self.maplayer_necessity = QgsMapLayerComboBox(self)

        layout.addRow("Possibility raster", self.maplayer_possibility)
        layout.addRow("Necessity raster", self.maplayer_necessity)

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

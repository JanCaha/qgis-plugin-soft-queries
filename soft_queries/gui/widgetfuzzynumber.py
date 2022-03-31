from pathlib import Path

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import (QComboBox, QStackedWidget, QTreeWidget, QLineEdit, QSpinBox,
                                 QLabel)

from processing.gui.wrappers import WidgetWrapper

path_file = Path(__file__)
path_widget_ui = path_file.parent / "widgetfuzzynumber.ui"
WIDGET, BASE = uic.loadUiType(path_widget_ui.absolute())


class FuzzyNumberWidget(BASE, WIDGET):

    fuzzy_type: QComboBox
    stackedWidget: QStackedWidget

    fuzzy_name: QLineEdit

    treeWidget: QTreeWidget

    alpha_cuts: QSpinBox
    label_alpha_cuts: QLabel

    triangular_min: QSpinBox
    triangular_midpoint: QSpinBox
    triangular_max: QSpinBox

    trapezoidal_min: QSpinBox
    trapezoidal_kernel_min: QSpinBox
    trapezoidal_kernel_max: QSpinBox
    trapezoidal_max: QSpinBox

    def __init__(self, parent=None) -> None:

        super(FuzzyNumberWidget, self).__init__(None)
        self.setupUi(self)

        self.fuzzy_type.addItems(["Triangular", "Trapezoidal"])
        self.change_fuzzy_def(0)
        self.fuzzy_type.currentIndexChanged.connect(self.change_fuzzy_def)

        self.alpha_cuts.setVisible(False)
        self.label_alpha_cuts.setVisible(False)

    def set_alpha_cuts_visibility(self, visibility: bool) -> None:

        self.alpha_cuts.setVisible(visibility)
        self.label_alpha_cuts.setVisible(visibility)

    def change_fuzzy_def(self, i: int) -> None:
        self.stackedWidget.setCurrentIndex(i)

    def setValue(self, value: str):

        split_value = value.split(";")

        fn_type = split_value[0]

        values = split_value[1].split("|")

        if fn_type == "triangular":

            self.fuzzy_type.setCurrentIndex(0)

            self.triangular_min.setValue(float(values[0]))
            self.triangular_midpoint.setValue(float(values[1]))
            self.triangular_max.setValue(float(values[2]))

        elif fn_type == "trapezoidal":

            self.fuzzy_type.setCurrentIndex(1)

            self.trapezoidal_min.setValue(float(values[0]))
            self.trapezoidal_kernel_min.setValue(float(values[1]))
            self.trapezoidal_kernel_max.setValue(float(values[2]))
            self.trapezoidal_max.setValue(float(values[3]))

    def value(self):

        if self.fuzzy_type.currentText().lower() == "triangular":

            return "triangular;{}|{}|{}".format(self.triangular_min.value(),
                                                self.triangular_midpoint.value(),
                                                self.triangular_max.value())

        elif self.fuzzy_type.currentText().lower() == "trapezoidal":

            return "trapezoidal;{}|{}|{}|{}".format(self.trapezoidal_min.value(),
                                                    self.trapezoidal_kernel_min.value(),
                                                    self.trapezoidal_kernel_max.value(),
                                                    self.trapezoidal_max.value())

    def value_as_dict(self):

        if self.fuzzy_type.currentText().lower() == "triangular":

            return {
                "fuzzy_number_type": "triangular",
                "alpha_cuts": int(self.alpha_cuts.value()),
                "min": self.triangular_min.value(),
                "midpoint": self.triangular_midpoint.value(),
                "max": self.triangular_max.value()
            }

        elif self.fuzzy_type.currentText().lower() == "trapezoidal":

            return {
                "fuzzy_number_type": "trapezoidal",
                "alpha_cuts": int(self.alpha_cuts.value()),
                "min": self.trapezoidal_min.value(),
                "kernel_min": self.trapezoidal_kernel_min.value(),
                "kernel_max": self.trapezoidal_kernel_max.value(),
                "max": self.trapezoidal_max.value()
            }


# https://github.com/qgis/QGIS/blob/master/python/plugins/processing/algs/qgis/ui/ReliefColorsWidget.py


class FuzzyNumberWidgetWrapper(WidgetWrapper):

    def createWidget(self):
        return FuzzyNumberWidget()

    def setValue(self, value):
        self.widget.setValue(value)

    def value(self):
        return self.widget.value()

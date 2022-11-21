from typing import Optional

from qgis.PyQt.QtWidgets import (QComboBox, QStackedWidget, QDoubleSpinBox, QLabel, QGroupBox,
                                 QFormLayout, QSpinBox, QWidget)

from processing.gui.wrappers import WidgetWrapper


class FuzzyNumberWidget(QGroupBox):

    def __init__(self, parent=None) -> None:

        super(FuzzyNumberWidget, self).__init__("Fuzzy Number Definition", parent)

        group_layout = QFormLayout(self)
        self.setLayout(group_layout)

        self.label_fuzzy_type = QLabel("Type of fuzzy number")
        self.fuzzy_type = QComboBox()

        self.label_alpha_cuts = QLabel("Number of alpha cuts")
        self.alpha_cuts = QSpinBox()
        self.alpha_cuts.setMinimum(1)
        self.alpha_cuts.setMaximum(50)
        self.alpha_cuts.setValue(1)

        self.label_number_decimals = QLabel("Number of decimals")
        self.number_decimals = QSpinBox()
        self.number_decimals.setMinimum(0)
        self.number_decimals.setMaximum(15)

        self.stacked_widget = QStackedWidget(self)

        group_layout.addRow(self.label_fuzzy_type, self.fuzzy_type)
        group_layout.addRow(self.label_number_decimals, self.number_decimals)
        group_layout.addRow(self.stacked_widget)
        group_layout.addRow(self.label_alpha_cuts, self.alpha_cuts)

        # page Triangular
        page_triangular = QWidget(self)
        self.stacked_widget.addWidget(page_triangular)
        layout = QFormLayout()
        page_triangular.setLayout(layout)

        label_triangular = QLabel("Triangular")
        self.triangular_min = DoubleSpinBox()
        self.triangular_midpoint = DoubleSpinBox()
        self.triangular_max = DoubleSpinBox()

        layout.addRow(label_triangular)
        layout.addRow("Minimum", self.triangular_min)
        layout.addRow("Midpoint", self.triangular_midpoint)
        layout.addRow("Maximum", self.triangular_max)

        # page Trapezoidal
        page_trapezoidal = QWidget(self)
        self.stacked_widget.addWidget(page_trapezoidal)
        layout = QFormLayout()
        page_trapezoidal.setLayout(layout)

        label_trapezoidal = QLabel("Trapezoidal")
        self.trapezoidal_min = DoubleSpinBox()
        self.trapezoidal_kernel_min = DoubleSpinBox()
        self.trapezoidal_kernel_max = DoubleSpinBox()
        self.trapezoidal_max = DoubleSpinBox()

        layout.addRow(label_trapezoidal)
        layout.addRow("Minimum", self.trapezoidal_min)
        layout.addRow("Kernel minimum", self.trapezoidal_kernel_min)
        layout.addRow("Kernel maximum", self.trapezoidal_kernel_max)
        layout.addRow("Maximum", self.trapezoidal_max)

        self.fuzzy_type.addItems(["Triangular", "Trapezoidal"])
        self.change_fuzzy_def(0)
        self.fuzzy_type.currentIndexChanged.connect(self.change_fuzzy_def)

        self.number_decimals.valueChanged.connect(self.set_decimals)
        self.number_decimals.setValue(3)

        self.triangular_min.valueChanged.connect(self.verify_triangular_values)
        self.triangular_midpoint.valueChanged.connect(self.verify_triangular_values)
        self.triangular_max.valueChanged.connect(self.verify_triangular_values)

        self.trapezoidal_min.valueChanged.connect(self.verify_trapezoidal_values)
        self.trapezoidal_kernel_min.valueChanged.connect(self.verify_trapezoidal_values)
        self.trapezoidal_kernel_max.valueChanged.connect(self.verify_trapezoidal_values)
        self.trapezoidal_max.valueChanged.connect(self.verify_trapezoidal_values)

        self.alpha_cuts.setVisible(False)
        self.label_alpha_cuts.setVisible(False)

    def set_decimals(self, decimals: int) -> None:
        self.triangular_min.setDecimals(decimals)
        self.triangular_midpoint.setDecimals(decimals)
        self.triangular_max.setDecimals(decimals)
        self.trapezoidal_min.setDecimals(decimals)
        self.trapezoidal_kernel_min.setDecimals(decimals)
        self.trapezoidal_kernel_max.setDecimals(decimals)
        self.trapezoidal_max.setDecimals(decimals)

    def verify_triangular_values(self):
        if self.triangular_min.value() > self.triangular_midpoint.value():
            self.triangular_midpoint.setValue(self.triangular_min.value())
        if self.triangular_midpoint.value() > self.triangular_max.value():
            self.triangular_max.setValue(self.triangular_midpoint.value())

    def verify_trapezoidal_values(self):
        if self.trapezoidal_min.value() > self.trapezoidal_kernel_min.value():
            self.trapezoidal_kernel_min.setValue(self.trapezoidal_min.value())
        if self.trapezoidal_kernel_min.value() > self.trapezoidal_kernel_max.value():
            self.trapezoidal_kernel_max.setValue(self.trapezoidal_kernel_min.value())
        if self.trapezoidal_kernel_max.value() > self.trapezoidal_max.value():
            self.trapezoidal_max.setValue(self.trapezoidal_kernel_max.value())

    def set_alpha_cuts_visibility(self, visibility: bool) -> None:

        self.alpha_cuts.setVisible(visibility)
        self.label_alpha_cuts.setVisible(visibility)

    def change_fuzzy_def(self, i: int) -> None:
        self.stacked_widget.setCurrentIndex(i)

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


class FuzzyNumberWidgetWrapper(WidgetWrapper):

    def createWidget(self):
        return FuzzyNumberWidget()

    def setValue(self, value):
        self.widget.setValue(value)

    def value(self):
        return self.widget.value()


class DoubleSpinBox(QDoubleSpinBox):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setMinimum(-999999999.999999)
        self.setMaximum(999999999.999999)
        self.setValue(0)
        self.setDecimals(6)

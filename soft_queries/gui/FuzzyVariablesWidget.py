from FuzzyMath.class_factories import FuzzyNumber, FuzzyNumberFactory
from qgis.core import QgsApplication
from qgis.PyQt.QtWidgets import (
    QDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QToolButton,
)

from ..text_constants import TextConstants
from .widgetfuzzynumber import FuzzyNumberWidget
from .widgetfuzzyvariables import FuzzyVariablesTreeWidget


class FuzzyVariablesWidget(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.init_gui()

    def init_gui(self) -> None:
        self.setWindowTitle(TextConstants.fuzzy_variables)

        layout = QGridLayout(self)
        self.setLayout(layout)

        self.label_name = QLabel("Fuzzy Variable Name")
        self.fuzzy_name = QLineEdit()

        layout.addWidget(self.label_name, 0, 0)
        layout.addWidget(self.fuzzy_name, 0, 1)

        self.widget_fuzzy_number = FuzzyNumberWidget()

        layout.addWidget(self.widget_fuzzy_number, 1, 0, 1, 2)

        lineLayout = QHBoxLayout()

        self.toolButton_add = QToolButton()
        self.toolButton_remove = QToolButton()

        lineLayout.addStretch(1)
        lineLayout.addWidget(self.toolButton_add)
        lineLayout.addWidget(self.toolButton_remove)
        layout.addLayout(lineLayout, 2, 1, 1, 1)

        self.treeWidget = FuzzyVariablesTreeWidget()

        layout.addWidget(self.treeWidget, 3, 0, 1, 2)

        self.toolButton_add.setIcon(QgsApplication.getThemeIcon("/symbologyAdd.svg"))
        self.toolButton_remove.setIcon(
            QgsApplication.getThemeIcon("/symbologyRemove.svg")
        )

        self.toolButton_add.clicked.connect(self.add_fuzzy_variable)
        self.toolButton_remove.clicked.connect(self.remove_fuzzy_variable)

    def add_fuzzy_variable(self) -> None:
        fuzzy_variable_name = self.fuzzy_name.text()

        if self.treeWidget.fuzzy_variable_exist(fuzzy_variable_name):
            dialog_error = QMessageBox()
            dialog_error.setIcon(QMessageBox.Critical)
            dialog_error.setText(
                "Cannot add `{}` as the fuzzy variable with the name already exist!".format(
                    fuzzy_variable_name
                )
            )
            dialog_error.setInformativeText("Please select another name.")
            dialog_error.setWindowTitle("Error")
            dialog_error.exec()

            return

        fn = self.fuzzy_number()
        self.treeWidget.database.add_fuzzy_variable(fuzzy_variable_name, fn)
        self.treeWidget.refresh()

    def remove_fuzzy_variable(self):
        fuzzy_number_name = self.treeWidget.current_fuzzy_number_name()

        if fuzzy_number_name:
            self.treeWidget.database.delete_fuzzy_variable(fuzzy_number_name)

        self.treeWidget.refresh()

    def fuzzy_number(self) -> FuzzyNumber:
        fn_def = self.widget_fuzzy_number.value_as_dict()

        if fn_def["fuzzy_number_type"] == "triangular":
            fn = FuzzyNumberFactory.triangular(
                fn_def["min"], fn_def["midpoint"], fn_def["max"], fn_def["alpha_cuts"]
            )

        elif fn_def["fuzzy_number_type"] == "trapezoidal":
            fn = FuzzyNumberFactory.trapezoidal(
                fn_def["min"],
                fn_def["kernel_min"],
                fn_def["kernel_max"],
                fn_def["max"],
                fn_def["alpha_cuts"],
            )

        return fn

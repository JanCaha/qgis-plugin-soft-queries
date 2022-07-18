from typing import List

from qgis.PyQt.QtWidgets import (QMessageBox, QToolButton, QTreeWidget, QTreeWidgetItem, QLineEdit,
                                 QSpinBox, QLabel, QGridLayout, QHBoxLayout, QSpacerItem, QDialog,
                                 QSizePolicy)
from qgis.PyQt.QtCore import pyqtSignal
from qgis.core import QgsApplication

from ..database.class_db import FuzzyDatabase
from ..text_constants import TextConstants

from ..FuzzyMath.class_factories import FuzzyNumberFactory, FuzzyNumber

from .widgetfuzzynumber import FuzzyNumberWidget


class FuzzyVariablesWidget(QDialog):

    def __init__(self, parent):
        super().__init__(parent)

        self.init_gui()

        self.fuzzy_variables_ids: List[str] = []

        self.database = FuzzyDatabase()

        data = self.database.get_fuzzy_variables()

        for name in data.keys():

            item = QTreeWidgetItem()
            item.setText(0, name)
            item.setText(1, str(data[name]))

            self.treeWidget.addTopLevelItem(item)

    def init_gui(self) -> None:
        self.setWindowTitle(TextConstants.fuzzy_variables)

        layout = QGridLayout(self)
        self.setLayout(layout)

        self.label_name = QLabel("Fuzzy variable name")
        self.fuzzy_name = QLineEdit()

        layout.addWidget(self.label_name, 0, 0)
        layout.addWidget(self.fuzzy_name, 0, 1)

        self.widget_fuzzy_number = FuzzyNumberWidget()

        layout.addWidget(self.widget_fuzzy_number, 1, 0, 1, 2)

        lineLayout = QHBoxLayout()

        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding)
        self.toolButton_add = QToolButton()
        self.toolButton_remove = QToolButton()

        lineLayout.addSpacerItem(spacer)
        lineLayout.addWidget(self.toolButton_add)
        lineLayout.addWidget(self.toolButton_remove)
        layout.addLayout(lineLayout, 2, 1, 1, 1)

        self.treeWidget = QTreeWidget()
        self.treeWidget.setHeaderLabels(["Fuzzy variable name", "Fuzzy variable"])

        layout.addWidget(self.treeWidget, 3, 0, 1, 2)

        self.toolButton_add.setIcon(QgsApplication.getThemeIcon('/symbologyAdd.svg'))
        self.toolButton_remove.setIcon(QgsApplication.getThemeIcon('/symbologyRemove.svg'))

        self.toolButton_add.clicked.connect(self.add_fuzzy_variable)
        self.toolButton_remove.clicked.connect(self.remove_fuzzy_variable)

    def change_fuzzy_def(self, i: int) -> None:
        self.stackedWidget.setCurrentIndex(i)

    def add_fuzzy_variable(self) -> None:

        fuzzy_variable_name = self.fuzzy_name.text()

        if self.check_fuzzy_variable_exit(fuzzy_variable_name):

            dialog_error = QMessageBox()
            dialog_error.setIcon(QMessageBox.Critical)
            dialog_error.setText(
                "Cannot add `{}` as the fuzzy variable with the name already exist!".format(
                    fuzzy_variable_name))
            dialog_error.setInformativeText("Please select another name.")
            dialog_error.setWindowTitle("Error")
            dialog_error.exec_()

            return

        item = QTreeWidgetItem()
        item.setText(0, fuzzy_variable_name)

        fn = self.get_fuzzy_number()

        item.setText(1, str(fn))

        self.database.add_fuzzy_variable(fuzzy_variable_name, fn)

        self.treeWidget.addTopLevelItem(item)

        self.regenerate_fuzzy_variables_ids()

    def remove_fuzzy_variable(self):

        item = self.treeWidget.currentItem()
        if not item:
            return

        self.database.delete_fuzzy_variable(item.text(0))

        self.treeWidget.invisibleRootItem().removeChild(item)

        self.regenerate_fuzzy_variables_ids()

    def check_fuzzy_variable_exit(self, fuzzy_variable_name: str) -> bool:

        return fuzzy_variable_name in self.fuzzy_variables_ids

    def regenerate_fuzzy_variables_ids(self) -> None:

        root = self.treeWidget.invisibleRootItem()

        child_count = root.childCount()

        self.fuzzy_variables_ids = [None] * child_count

        for i in range(child_count):

            item = root.child(i)

            self.fuzzy_variables_ids[i] = item.text(0)

    def get_fuzzy_number(self) -> FuzzyNumber:

        fn_def = self.widget_fuzzy_number.value_as_dict()

        if fn_def["fuzzy_number_type"] == "triangular":

            fn = FuzzyNumberFactory.triangular(fn_def["min"], fn_def["midpoint"], fn_def["max"],
                                               fn_def["alpha_cuts"])

        elif fn_def["fuzzy_number_type"] == "trapezoidal":

            fn = FuzzyNumberFactory.trapezoidal(fn_def["min"], fn_def["kernel_min"],
                                                fn_def["kernel_max"], fn_def["max"],
                                                fn_def["alpha_cuts"])

        return fn

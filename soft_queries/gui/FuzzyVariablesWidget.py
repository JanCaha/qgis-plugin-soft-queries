from pathlib import Path
from typing import List

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import (QMessageBox, QToolButton, QComboBox, QStackedWidget, QTreeWidget,
                                 QTreeWidgetItem, QLineEdit, QSpinBox, QLabel)
from qgis.PyQt.QtCore import pyqtSignal
from qgis.core import QgsApplication

from ..database.class_db import FuzzyDatabase
from ..text_constants import TextConstants

from ..FuzzyMath.class_factories import FuzzyNumberFactory

path_ui = Path(__file__).parent / "dialogcreatefuzzyrecord.ui"
WIDGET, BASE = uic.loadUiType(path_ui.as_posix())


class FuzzyVariablesWidget(BASE, WIDGET):

    toolButton_add: QToolButton
    toolButton_remove: QToolButton

    fuzzy_type: QComboBox
    stackedWidget: QStackedWidget

    fuzzy_name: QLineEdit

    treeWidget: QTreeWidget

    alpha_cuts: QSpinBox
    label_alpha_cuts: QLabel

    data_has_changed = pyqtSignal()

    fuzzy_variables_ids: List[str] = []

    def __init__(self, parent):

        super().__init__(parent)

        self.setupUi(self)

        self.setWindowTitle(TextConstants.fuzzy_variables)

        self.toolButton_add.setIcon(QgsApplication.getThemeIcon('/symbologyAdd.svg'))
        self.toolButton_remove.setIcon(QgsApplication.getThemeIcon('/symbologyRemove.svg'))

        self.toolButton_add.clicked.connect(self.add_fuzzy_variable)
        self.toolButton_remove.clicked.connect(self.remove_fuzzy_variable)

        self.fuzzy_type.addItems(["Triangular", "Trapezoidal"])
        self.change_fuzzy_def(0)
        self.fuzzy_type.currentIndexChanged.connect(self.change_fuzzy_def)

        self.alpha_cuts.setVisible(False)
        self.label_alpha_cuts.setVisible(False)

        self.data_has_changed.connect(self.regenerate_fuzzy_variables_ids)

        self.database = FuzzyDatabase()

        data = self.database.get_fuzzy_variables()

        for name in data.keys():

            item = QTreeWidgetItem()
            item.setText(0, name)
            item.setText(1, str(data[name]))

            self.treeWidget.addTopLevelItem(item)

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

        if self.fuzzy_type.currentIndex() == 0:
            fn = FuzzyNumberFactory.triangular(self.triangular_min.value(),
                                               self.triangular_midpoint.value(),
                                               self.triangular_max.value(),
                                               number_of_cuts=self.alpha_cuts.value())
            item.setText(1, str(fn))

            self.database.add_fuzzy_variable(fuzzy_variable_name, fn)

        else:
            item.setText(1, "aaa")

        self.treeWidget.addTopLevelItem(item)

        self.data_has_changed.emit()

    def remove_fuzzy_variable(self):

        item = self.treeWidget.currentItem()
        if not item:
            return

        self.database.delete_fuzzy_variable(item.text(0))

        self.treeWidget.invisibleRootItem().removeChild(item)

        self.data_has_changed.emit()

    def check_fuzzy_variable_exit(self, fuzzy_variable_name: str) -> bool:

        return fuzzy_variable_name in self.fuzzy_variables_ids

    def regenerate_fuzzy_variables_ids(self) -> None:

        root = self.treeWidget.invisibleRootItem()

        child_count = root.childCount()

        self.fuzzy_variables_ids = [None] * child_count

        for i in range(child_count):

            item = root.child(i)

            self.fuzzy_variables_ids[i] = item.text(0)

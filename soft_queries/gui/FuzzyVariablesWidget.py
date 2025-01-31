import shutil
from pathlib import Path

from FuzzyMath.class_factories import FuzzyNumber, FuzzyNumberFactory
from qgis.core import QgsApplication
from qgis.PyQt.QtWidgets import QDialog, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QToolButton

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

        line_layout = QHBoxLayout()

        self.tool_button_add = QToolButton()
        self.tool_button_add.setEnabled(False)
        self.tool_button_add.setToolTip("Add Fuzzy Variable")
        self.tool_button_remove = QToolButton()
        self.tool_button_remove.setToolTip("Remove Fuzzy Variable")
        self.tool_button_clean = QToolButton()
        self.tool_button_clean.setToolTip("Clean All Fuzzy Variables")

        line_layout.addStretch(1)
        line_layout.addWidget(self.tool_button_add)
        line_layout.addWidget(self.tool_button_remove)
        line_layout.addWidget(self.tool_button_clean)
        layout.addLayout(line_layout, 2, 1, 1, 1)

        self.tree_widget = FuzzyVariablesTreeWidget()

        layout.addWidget(self.tree_widget, 3, 0, 1, 2)

        self.tool_button_add.setIcon(QgsApplication.getThemeIcon("/symbologyAdd.svg"))
        self.tool_button_remove.setIcon(QgsApplication.getThemeIcon("/symbologyRemove.svg"))
        self.tool_button_clean.setIcon(QgsApplication.getThemeIcon("/mActionDeleteSelected.svg"))

        self.tool_button_add.clicked.connect(self.add_fuzzy_variable)
        self.tool_button_remove.clicked.connect(self.remove_fuzzy_variable)
        self.tool_button_clean.clicked.connect(self._empty_db_file)
        self.fuzzy_name.textChanged.connect(self.activate_addition)
        self.tree_widget.currentItemChanged.connect(self.activate_deletion)

    def add_fuzzy_variable(self) -> None:
        fuzzy_variable_name = self.fuzzy_name.text()

        if self.tree_widget.fuzzy_variable_exist(fuzzy_variable_name):
            dialog_error = QMessageBox()
            dialog_error.setIcon(QMessageBox.Icon.Critical)
            dialog_error.setText(
                f"Cannot add `{fuzzy_variable_name}` as the fuzzy variable with the name already exist!"
            )
            dialog_error.setInformativeText("Please select another name.")
            dialog_error.setWindowTitle("Cannot Add Fuzzy Variable")
            dialog_error.exec()

            return

        fn = self.fuzzy_number()
        self.tree_widget.database.add_fuzzy_variable(fuzzy_variable_name, fn)
        self.tree_widget.refresh()

    def remove_fuzzy_variable(self):
        fuzzy_number_name = self.tree_widget.current_fuzzy_number_name()

        if fuzzy_number_name:
            self.tree_widget.database.delete_fuzzy_variable(fuzzy_number_name)

        self.tree_widget.refresh()

    def fuzzy_number(self) -> FuzzyNumber:
        fn_def = self.widget_fuzzy_number.value_as_dict()

        if fn_def["fuzzy_number_type"] == "triangular":
            fn = FuzzyNumberFactory.triangular(fn_def["min"], fn_def["midpoint"], fn_def["max"], fn_def["alpha_cuts"])

        elif fn_def["fuzzy_number_type"] == "trapezoidal":
            fn = FuzzyNumberFactory.trapezoidal(
                fn_def["min"],
                fn_def["kernel_min"],
                fn_def["kernel_max"],
                fn_def["max"],
                fn_def["alpha_cuts"],
            )

        return fn

    def activate_addition(self) -> None:
        if len(self.fuzzy_name.text().strip()) == 0:
            self.tool_button_add.setEnabled(False)
        else:
            self.tool_button_add.setEnabled(True)

    def activate_deletion(self) -> None:
        if self.tree_widget.currentIndex().row() == -1:
            self.tool_button_remove.setEnabled(False)
        else:
            self.tool_button_remove.setEnabled(True)

    def _empty_db_file(self) -> None:

        msg_box = QMessageBox(self.parent())
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setWindowTitle("Empty Fuzzy Numbers Database")
        msg_box.setText("Remove all fuzzy variables from the database?")
        msg_box.setStandardButtons(QMessageBox.StandardButton.No | QMessageBox.StandardButton.Yes)
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)
        res = msg_box.exec_()
        if res == QMessageBox.StandardButton.Yes:
            path_db = Path(__file__).parent.parent / "database" / "plugin.db"
            path_empty_db = Path(__file__).parent.parent / "database" / "empty_backup.db"

            shutil.copyfile(path_empty_db, path_db)

            self.tree_widget.refresh()

from typing import List, Optional

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QTreeWidget, QTreeWidgetItem, QWidget

from ..database.class_db import FuzzyDatabase
from ..FuzzyMath import FuzzyNumber


class FuzzyVariablesTreeWidget(QTreeWidget):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self._database = FuzzyDatabase()

        self.setHeaderLabels(["Variable name", "Fuzzy variable"])

        self.refresh()

    def refresh(self):

        data = self._database.get_fuzzy_variables()

        self.clear()

        for name in data.keys():

            item = QTreeWidgetItem()
            item.setText(0, name)
            item.setText(1, str(data[name]))
            item.setData(0, Qt.UserRole, data[name])

            self.addTopLevelItem(item)

    @property
    def database(self) -> FuzzyDatabase:
        return self._database

    @property
    def fuzzy_variables_ids(self) -> List[str]:
        root = self.invisibleRootItem()

        child_count = root.childCount()

        fuzzy_variables_ids = [""] * child_count

        for i in range(child_count):

            item = root.child(i)

            fuzzy_variables_ids[i] = item.text(0)

        return fuzzy_variables_ids

    def current_fuzzy_number(self) -> FuzzyNumber:
        item = self.currentItem()
        if item:
            return item.data(0, Qt.UserRole)
        else:
            return None

    def current_fuzzy_number_name(self) -> str:
        item = self.currentItem()
        if item:
            return item.text(0)
        else:
            return None

    def fuzzy_variable_exist(self, fuzzy_variable_name: str) -> bool:
        return fuzzy_variable_name in self.fuzzy_variables_ids

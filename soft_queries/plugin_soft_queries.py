import inspect
import os
import sys

from qgis.core import QgsApplication, QgsExpression
from qgis.gui import QgisInterface
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from .expressions.expressions_fuzzy_comparisons import (
    possibilistic_exceedance,
    possibilistic_strict_exceedance,
    possibilistic_strict_undervaluation,
    possibilistic_undervaluation,
)
from .expressions.expressions_fuzzy_membership import (
    calculate_fuzzy_membership,
    fuzzy_and,
    fuzzy_membership,
    fuzzy_or,
    membership,
)
from .expressions.expressions_fuzzy_number import (
    fuzzy_number_trapezoidal,
    fuzzy_number_triangular,
    get_fuzzy_number_from_db,
)
from .expressions.expressions_general import sq_as_string, sq_from_string_repr, sq_to_string_repr
from .expressions.expressions_possibilistic_membership import (
    necessity,
    possibilistic_and,
    possibilistic_membership,
    possibilistic_or,
    possibility,
)
from .gui.FuzzyVariablesWidget import FuzzyVariablesWidget
from .provider_soft_queries import SoftQueriesProvider
from .text_constants import TextConstants
from .utils import get_icon_path

cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]

if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)


class SoftQueriesPlugin:
    def __init__(self, iface):

        self.iface: QgisInterface = iface

        self.provider = SoftQueriesProvider()

        self.tool = None

        self.actions = []
        self.menu = TextConstants.plugin_name

        self.exp_functions = [
            # sq general
            sq_as_string,
            sq_from_string_repr,
            sq_to_string_repr,
            # fuzzy numbers
            fuzzy_number_triangular,
            fuzzy_number_trapezoidal,
            get_fuzzy_number_from_db,
            # fuzzy membership
            fuzzy_membership,
            fuzzy_and,
            fuzzy_or,
            membership,
            calculate_fuzzy_membership,
            # possibilistic membership
            possibilistic_membership,
            possibility,
            necessity,
            possibilistic_and,
            possibilistic_or,
            # possibilistic comparison
            possibilistic_exceedance,
            possibilistic_strict_exceedance,
            possibilistic_undervaluation,
            possibilistic_strict_undervaluation,
        ]

        self.register_exp_functions()

    def initProcessing(self):
        QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        self.initProcessing()

        self.add_action(
            icon_path=get_icon_path("soft_queries.svg"),
            text=TextConstants.fuzzy_variables,
            callback=self.run_tool_fuzzy_variables,
            add_to_toolbar=True,
        )

    def run_tool_fuzzy_variables(self):

        widget = FuzzyVariablesWidget(self.iface.mainWindow())

        widget.exec_()

    def unload(self):
        QgsApplication.processingRegistry().removeProvider(self.provider)

        for action in self.actions:
            self.iface.removePluginMenu(TextConstants.plugin_name, action)
            self.iface.removeToolBarIcon(action)

        self.unregister_exp_functions()

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None,
        add_to_specific_toolbar=None,
    ):

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(self.menu, action)

        if add_to_specific_toolbar:
            add_to_specific_toolbar.addAction(action)

        self.actions.append(action)

        return action

    def register_exp_functions(self):

        for f in self.exp_functions:
            QgsExpression.registerFunction(f)

    def unregister_exp_functions(self):

        for f in self.exp_functions:
            QgsExpression.unregisterFunction(f.function.__name__)

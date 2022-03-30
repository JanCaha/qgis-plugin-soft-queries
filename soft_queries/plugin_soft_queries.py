import os
import sys
import inspect

from qgis.core import (QgsApplication, QgsExpression)
from qgis.gui import (QgisInterface)
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from .provider_soft_queries import SoftQueriesProvider
from .text_constants import TextConstants
from .expressions.expressions_fuzzy_number import (fuzzy_number_triangular,
                                                   fuzzy_number_trapezoidal,
                                                   fuzzy_number_to_string_repr,
                                                   fuzzy_number_from_string_repr,
                                                   fuzzy_number_as_text, get_fuzzy_number_from_db)
from .expressions.expressions_fuzzy_membership import (fuzzy_membership, fuzzy_membership_as_text,
                                                       fuzzy_membership_to_string_repr,
                                                       fuzzy_membership_from_string_repr,
                                                       fuzzy_and, fuzzy_or, membership)
from .expressions.expressions_possibilistic_membership import (
    possibilistic_membership_as_text, possibilistic_membership_to_string_repr,
    possibilistic_membership_from_string_repr, possibilistic_membership, possibility, necessity,
    possibilistic_and, possibilistic_or, possibilistic_exceedance, possibilistic_strict_exceedance,
    possibilistic_undervaluation, possibilistic_strict_undervaluation)

cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]

if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)


class FuzzyClassifierPlugin():

    def __init__(self, iface):

        self.iface: QgisInterface = iface

        self.provider = SoftQueriesProvider()

        self.tool = None

        self.actions = []
        self.menu = TextConstants.plugin_name

        self.register_exp_functions()

    def initProcessing(self):
        QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        self.initProcessing()

        self.add_action(
            icon_path=None,
            # icon_path=get_icon_path("qmapshaper.png"),
            text=TextConstants.fuzzy_variables,
            callback=self.run_tool_fuzzy_variables,
            add_to_toolbar=True)

    def run_tool_fuzzy_variables(self):
        from .gui.FuzzyVariablesWidget import FuzzyVariablesWidget

        widget = FuzzyVariablesWidget(self.iface.mainWindow())

        widget.exec_()

    def unload(self):
        QgsApplication.processingRegistry().removeProvider(self.provider)

        for action in self.actions:
            self.iface.removePluginMenu(TextConstants.plugin_name, action)
            self.iface.removeToolBarIcon(action)

        self.unregister_exp_functions()

    def add_action(self,
                   icon_path,
                   text,
                   callback,
                   enabled_flag=True,
                   add_to_menu=True,
                   add_to_toolbar=True,
                   status_tip=None,
                   whats_this=None,
                   parent=None,
                   add_to_specific_toolbar=None):

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

        # fuzzy numbers
        QgsExpression.registerFunction(fuzzy_number_triangular)
        QgsExpression.registerFunction(fuzzy_number_trapezoidal)
        QgsExpression.registerFunction(fuzzy_number_from_string_repr)
        QgsExpression.registerFunction(fuzzy_number_to_string_repr)
        QgsExpression.registerFunction(fuzzy_number_as_text)
        QgsExpression.registerFunction(get_fuzzy_number_from_db)

        # fuzzy membership
        QgsExpression.registerFunction(fuzzy_membership)
        QgsExpression.registerFunction(fuzzy_membership_as_text)
        QgsExpression.registerFunction(fuzzy_membership_to_string_repr)
        QgsExpression.registerFunction(fuzzy_membership_from_string_repr)
        QgsExpression.registerFunction(fuzzy_and)
        QgsExpression.registerFunction(fuzzy_or)
        QgsExpression.registerFunction(membership)

        # possibilistic membership
        QgsExpression.registerFunction(possibilistic_membership_as_text)
        QgsExpression.registerFunction(possibilistic_membership_to_string_repr)
        QgsExpression.registerFunction(possibilistic_membership_from_string_repr)
        QgsExpression.registerFunction(possibilistic_membership)
        QgsExpression.registerFunction(possibility)
        QgsExpression.registerFunction(necessity)
        QgsExpression.registerFunction(possibilistic_and)
        QgsExpression.registerFunction(possibilistic_or)
        QgsExpression.registerFunction(possibilistic_exceedance)
        QgsExpression.registerFunction(possibilistic_strict_exceedance)
        QgsExpression.registerFunction(possibilistic_undervaluation)
        QgsExpression.registerFunction(possibilistic_strict_undervaluation)

    def unregister_exp_functions(self):

        # fuzzy numbers
        QgsExpression.unregisterFunction('fuzzy_number_triangular')
        QgsExpression.unregisterFunction('fuzzy_number_trapezoidal')
        QgsExpression.unregisterFunction('fuzzy_number_from_string_repr')
        QgsExpression.unregisterFunction('fuzzy_number_to_string_repr')
        QgsExpression.unregisterFunction('fuzzy_number_as_text')
        QgsExpression.unregisterFunction('get_fuzzy_number_from_db')

        # fuzzy membership
        QgsExpression.unregisterFunction('fuzzy_membership')
        QgsExpression.unregisterFunction('fuzzy_membership_as_text')
        QgsExpression.unregisterFunction('fuzzy_membership_to_string_repr')
        QgsExpression.unregisterFunction('fuzzy_membership_from_string_repr')
        QgsExpression.unregisterFunction('fuzzy_and')
        QgsExpression.unregisterFunction('fuzzy_or')
        QgsExpression.unregisterFunction('membership')

        # possibilistic membership
        QgsExpression.unregisterFunction('possibilistic_membership_as_text')
        QgsExpression.unregisterFunction('possibilistic_membership_to_string_repr')
        QgsExpression.unregisterFunction('possibilistic_membership_from_string_repr')
        QgsExpression.unregisterFunction('possibilistic_membership')
        QgsExpression.unregisterFunction('possibility')
        QgsExpression.unregisterFunction('necessity')
        QgsExpression.unregisterFunction('possibilistic_and')
        QgsExpression.unregisterFunction('possibilistic_or')
        QgsExpression.unregisterFunction('possibilistic_exceedance')
        QgsExpression.unregisterFunction('possibilistic_strict_exceedance')
        QgsExpression.unregisterFunction('possibilistic_undervaluation')
        QgsExpression.unregisterFunction('possibilistic_strict_undervaluation')

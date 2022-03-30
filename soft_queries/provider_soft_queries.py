from pathlib import Path
import configparser

from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsProcessingProvider

from .text_constants import TextConstants
from .processing.tool_possibilistic_membership import PossibilisticMembershipAlgorithm
from .processing.tool_fuzzy_membership import FuzzyMembershipAlgorithm
from .processing.tool_fuzzy_operation import FuzzyOperationAlgorithm


class SoftQueriesProvider(QgsProcessingProvider):

    def __init__(self):
        super().__init__()

        path = Path(__file__).parent / 'metadata.txt'

        config = configparser.ConfigParser()
        config.read(path)

        self.version = config['general']['version']

    def load(self) -> bool:

        self.refreshAlgorithms()

        return True

    def versionInfo(self):
        return self.version

    def loadAlgorithms(self):
        self.addAlgorithm(PossibilisticMembershipAlgorithm())
        self.addAlgorithm(FuzzyMembershipAlgorithm())
        self.addAlgorithm(FuzzyOperationAlgorithm())

    def id(self):
        return TextConstants.plugin_id

    def name(self):
        return TextConstants.plugin_name

    # def icon(self):
    #     path = Path(__file__).parent / "icons" / ""
    #     return QIcon(str(path))

    def longName(self):
        return self.name()

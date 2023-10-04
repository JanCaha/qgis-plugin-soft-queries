import configparser
from pathlib import Path

from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon

from .processing.tool_fuzzy_membership import FuzzyMembershipAlgorithm
from .processing.tool_fuzzy_operation import FuzzyOperationAlgorithm
from .processing.tool_possibilistic_membership import PossibilisticMembershipAlgorithm
from .processing.tool_possibilistic_operation import PossibilisticOperationAlgorithm
from .text_constants import TextConstants
from .utils import get_icon_path


class SoftQueriesProvider(QgsProcessingProvider):
    def __init__(self):
        super().__init__()

        path = Path(__file__).parent / "metadata.txt"

        config = configparser.ConfigParser()
        config.read(path)

        self.version = config["general"]["version"]

    def load(self) -> bool:

        self.refreshAlgorithms()

        return True

    def versionInfo(self):
        return self.version

    def loadAlgorithms(self):
        self.addAlgorithm(PossibilisticMembershipAlgorithm())
        self.addAlgorithm(FuzzyMembershipAlgorithm())
        self.addAlgorithm(FuzzyOperationAlgorithm())
        self.addAlgorithm(PossibilisticOperationAlgorithm())

    def id(self):
        return TextConstants.plugin_id

    def name(self):
        return TextConstants.plugin_name

    def icon(self):
        return QIcon(get_icon_path("soft_queries.svg"))

    def longName(self):
        return self.name()

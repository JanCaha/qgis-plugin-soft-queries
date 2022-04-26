from typing import Tuple

from qgis.core import QgsProcessingParameterDefinition, QgsRasterLayer


class ParameterPossibilisticElement(QgsProcessingParameterDefinition):

    def __init__(self, name='', description='', parent=None, optional=False):
        super().__init__(name, description, None, optional)
        self.parent = parent
        self.setMetadata({
            'widget_wrapper':
                'soft_queries.gui.widgetpossibilisticelement.PossibilisticElementWidgetWrapper'
        })

    def type(self):
        return 'possibilistic_element'

    def clone(self):
        return ParameterPossibilisticElement(
            self.name(), self.description(), self.parent,
            self.flags() & QgsProcessingParameterDefinition.FlagOptional)

    @staticmethod
    def valueToRasters(value: str) -> Tuple[QgsRasterLayer, QgsRasterLayer]:
        if value is None:
            return None

        if value == '':
            return None

        if isinstance(value, str):

            split_value = value.split("::~::")

            raster_possibility = QgsRasterLayer(split_value[0])
            raster_necessity = QgsRasterLayer(split_value[1])

            return (raster_possibility, raster_necessity)

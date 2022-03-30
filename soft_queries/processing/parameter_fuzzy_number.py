from qgis.core import QgsProcessingParameterDefinition

from ..FuzzyMath import FuzzyNumberFactory


class ParameterFuzzyNumber(QgsProcessingParameterDefinition):

    def __init__(self, name='', description='', parent=None, optional=False):
        super().__init__(name, description, None, optional)
        self.parent = parent
        self.setMetadata(
            {'widget_wrapper': 'softqueries.gui.widgetfuzzynumber.FuzzNumberWidgetWrapper'})

    def type(self):
        return 'fuzzy_number'

    def clone(self):
        return ParameterFuzzyNumber(self.name(), self.description(), self.parent,
                                    self.flags() & QgsProcessingParameterDefinition.FlagOptional)

    @staticmethod
    def valueToFuzzyNumber(value):
        if value is None:
            return None

        if value == '':
            return None

        if isinstance(value, str):

            split_value = value.split(";")

            fn_type = split_value[0]

            values = split_value[1].split("|")

            if fn_type == "triangular":
                return FuzzyNumberFactory.triangular(float(values[0]), float(values[1]),
                                                     float(values[2]))

            elif fn_type == "trapezoidal":
                return FuzzyNumberFactory.trapezoidal(float(values[0]), float(values[1]),
                                                      float(values[2]), float(values[3]))

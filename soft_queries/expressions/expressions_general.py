from typing import Any, Union

from qgis.core import QgsExpression, QgsFeature, qgsfunction

from ..FuzzyMath import FuzzyMembership, FuzzyNumber, PossibilisticMembership
from ..text_constants import TextConstants
from ..utils import python_object_to_string, string_to_python_object
from .qgsexpressions_utils import load_help

FUZZY_NUMBER_STRING = "fuzzy_number_"
FUZZY_MEMBERSHIP_STRING = "fuzzy_membership_"
POSSIBILISTIC_MEMBERSHIP_STRING = "possibilistic_membership_"


def prepare_error_message(
        object: Any,
        parameter_name: str = "sq_object",
        class_name: str = "FuzzyNumber, FuzzyMembership, PossibilisticMembership") -> str:

    return "Parameter `{}` needs to be of classes `{}` but it is `{}`.".\
        format(parameter_name, class_name, type(object).__name__)


@qgsfunction(args="auto",
             group=TextConstants.exp_funcs_group,
             helpText=load_help("sq_to_string_repr"),
             register=False)
def sq_to_string_repr(sq_object: Union[FuzzyNumber, FuzzyMembership, PossibilisticMembership],
                      feature: QgsFeature, parent: QgsExpression):

    if isinstance(sq_object, FuzzyNumber):
        return python_object_to_string(sq_object, FUZZY_NUMBER_STRING)

    if isinstance(sq_object, FuzzyMembership):
        return python_object_to_string(sq_object, FUZZY_MEMBERSHIP_STRING)

    if isinstance(sq_object, PossibilisticMembership):

        return python_object_to_string(sq_object, POSSIBILISTIC_MEMBERSHIP_STRING)

    else:
        raise Exception(prepare_error_message(sq_object))


@qgsfunction(args="auto",
             group=TextConstants.exp_funcs_group,
             helpText=load_help("sq_as_string"),
             register=False)
def sq_as_string(sq_object: Union[FuzzyNumber, FuzzyMembership, PossibilisticMembership],
                 feature: QgsFeature, parent: QgsExpression):

    if isinstance(sq_object, FuzzyNumber):
        return str(sq_object)

    if isinstance(sq_object, FuzzyMembership):
        return repr(sq_object)

    if isinstance(sq_object, PossibilisticMembership):

        return repr(sq_object)

    else:
        raise Exception(prepare_error_message(sq_object))


@qgsfunction(args='auto',
             group=TextConstants.exp_funcs_group,
             helpText=load_help("sq_from_string_repr"),
             register=False)
def sq_from_string_repr(sq_string_object: str, feature: QgsFeature, parent: QgsExpression):

    if isinstance(sq_string_object, str) and sq_string_object.startswith(FUZZY_NUMBER_STRING):
        return string_to_python_object(sq_string_object, FUZZY_NUMBER_STRING)

    if isinstance(sq_string_object, str) and sq_string_object.startswith(FUZZY_MEMBERSHIP_STRING):
        return string_to_python_object(sq_string_object, FUZZY_MEMBERSHIP_STRING)

    if isinstance(sq_string_object, str) and\
            sq_string_object.startswith(POSSIBILISTIC_MEMBERSHIP_STRING):

        return string_to_python_object(sq_string_object, POSSIBILISTIC_MEMBERSHIP_STRING)

    else:
        raise Exception(prepare_error_message(sq_string_object, "str (with correct prefix)"))

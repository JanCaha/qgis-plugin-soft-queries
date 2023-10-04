from typing import Any, Tuple, Union

from qgis.core import QgsExpression, QgsFeature, qgsfunction

from ..FuzzyMath import FuzzyNumber, FuzzyNumberFactory
from ..text_constants import TextConstants
from .qgsexpressions_utils import error_message, load_help

FUZZY_NUMERICS = Union[FuzzyNumber, int, float]


def prepare_error_message(
    object: Any, parameter_name: str, class_name: str = "FuzzyNumber, int, float"
) -> str:
    return error_message(parameter_name, class_name, object)


@qgsfunction(
    args="auto",
    group=TextConstants.exp_funcs_group,
    helpText=load_help("possibilistic_exceedance"),
    register=False,
)
def possibilistic_exceedance(
    fn_1: FUZZY_NUMERICS,
    fn_2: FUZZY_NUMERICS,
    feature: QgsFeature,
    parent: QgsExpression,
):

    _validateInputs(fn_1, fn_2)

    fn_1, fn_2 = _returnAsFuzzyNumbers(fn_1, fn_2)

    return fn_1.exceedance(fn_2)


@qgsfunction(
    args="auto",
    group=TextConstants.exp_funcs_group,
    helpText=load_help("possibilistic_undervaluation"),
    register=False,
)
def possibilistic_undervaluation(
    fn_1: FUZZY_NUMERICS,
    fn_2: FUZZY_NUMERICS,
    feature: QgsFeature,
    parent: QgsExpression,
):

    _validateInputs(fn_1, fn_2)

    fn_1, fn_2 = _returnAsFuzzyNumbers(fn_1, fn_2)

    return fn_1.undervaluation(fn_2)


@qgsfunction(
    args="auto",
    group=TextConstants.exp_funcs_group,
    helpText=load_help("possibilistic_strict_exceedance"),
    register=False,
)
def possibilistic_strict_exceedance(
    fn_1: FUZZY_NUMERICS,
    fn_2: FUZZY_NUMERICS,
    feature: QgsFeature,
    parent: QgsExpression,
):

    _validateInputs(fn_1, fn_2)

    fn_1, fn_2 = _returnAsFuzzyNumbers(fn_1, fn_2)

    return fn_1.strict_exceedance(fn_2)


@qgsfunction(
    args="auto",
    group=TextConstants.exp_funcs_group,
    helpText=load_help("possibilistic_strict_undervaluation"),
    register=False,
)
def possibilistic_strict_undervaluation(
    fn_1: FUZZY_NUMERICS,
    fn_2: FUZZY_NUMERICS,
    feature: QgsFeature,
    parent: QgsExpression,
):

    _validateInputs(fn_1, fn_2)

    fn_1, fn_2 = _returnAsFuzzyNumbers(fn_1, fn_2)

    return fn_1.strict_undervaluation(fn_2)


def _returnAsFuzzyNumbers(
    fn_1: FUZZY_NUMERICS, fn_2: FUZZY_NUMERICS
) -> Tuple[FuzzyNumber, FuzzyNumber]:

    if isinstance(fn_1, (int, float)):
        fn_1 = FuzzyNumberFactory.crisp_number(fn_1)

    if isinstance(fn_2, (int, float)):
        fn_2 = FuzzyNumberFactory.crisp_number(fn_2)

    return (fn_1, fn_2)


def _validateInputs(fn_1: FUZZY_NUMERICS, fn_2: FUZZY_NUMERICS) -> None:

    if not isinstance(fn_1, (FuzzyNumber, int, float)):
        raise Exception(prepare_error_message(fn_1, "fn_1"))

    if not isinstance(fn_2, (FuzzyNumber, int, float)):
        raise Exception(prepare_error_message(fn_2, "fn_2"))

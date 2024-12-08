from typing import Any, Union

from FuzzyMath import PossibilisticAnd, PossibilisticMembership, PossibilisticOr
from FuzzyMath.class_membership_operations import FUZZY_AND_NAMES, FUZZY_OR_NAMES, FuzzyAnd, FuzzyOr
from qgis.core import QgsExpression, QgsFeature, qgsfunction

from ..text_constants import TextConstants
from .expressions_fuzzy_membership import prepare_type_error_message
from .qgsexpressions_utils import error_message, load_help


def prepare_error_message(
    object: Any,
    parameter_name: str = "possibilistic_membership",
    class_name: str = "PossibilisticMembership",
) -> str:
    return error_message(parameter_name, class_name, object)


@qgsfunction(
    args="auto",
    group=TextConstants.exp_funcs_group,
    helpText=load_help("possibilistic_membership"),
    register=False,
)
def possibilistic_membership(
    possibility: Union[int, float],
    necessity: Union[int, float],
    feature: QgsFeature,
    parent: QgsExpression,
):
    if not isinstance(possibility, (int, float)):
        raise TypeError(prepare_error_message(possibility, "possibility", "int, float"))

    if not isinstance(necessity, (int, float)):
        raise TypeError(prepare_error_message(necessity, "necessity", "int, float"))

    pm = PossibilisticMembership(possibility, necessity)

    return pm


@qgsfunction(
    args="auto",
    group=TextConstants.exp_funcs_group,
    helpText=load_help("possibility"),
    register=False,
)
def possibility(
    possibilistic_membership: PossibilisticMembership,
    feature: QgsFeature,
    parent: QgsExpression,
):
    if isinstance(possibilistic_membership, PossibilisticMembership):
        return possibilistic_membership.possibility

    else:
        raise TypeError(prepare_error_message(possibilistic_membership))


@qgsfunction(
    args="auto",
    group=TextConstants.exp_funcs_group,
    helpText=load_help("necessity"),
    register=False,
)
def necessity(
    possibilistic_membership: PossibilisticMembership,
    feature: QgsFeature,
    parent: QgsExpression,
):
    if isinstance(possibilistic_membership, PossibilisticMembership):
        return possibilistic_membership.necessity

    else:
        raise TypeError(prepare_error_message(possibilistic_membership))


@qgsfunction(
    args="auto",
    group=TextConstants.exp_funcs_group,
    helpText=load_help("possibilistic_and"),
    register=False,
)
def possibilistic_and(
    possibilistic_membership1: PossibilisticMembership,
    possibilistic_membership2: PossibilisticMembership,
    type: FuzzyAnd,
    feature: QgsFeature,
    parent: QgsExpression,
):
    if not isinstance(possibilistic_membership1, PossibilisticMembership):
        raise TypeError(prepare_error_message(possibilistic_membership1, "possibilistic_membership1"))

    if not isinstance(possibilistic_membership2, PossibilisticMembership):
        raise TypeError(prepare_error_message(possibilistic_membership2, "possibilistic_membership2"))

    if not (isinstance(type, str) and type in FUZZY_AND_NAMES):
        raise TypeError(prepare_type_error_message(type, FUZZY_AND_NAMES))

    return PossibilisticAnd.possibilisticAnd(possibilistic_membership1, possibilistic_membership2, type=type)


@qgsfunction(
    args="auto",
    group=TextConstants.exp_funcs_group,
    helpText=load_help("possibilistic_or"),
    register=False,
)
def possibilistic_or(
    possibilistic_membership1: PossibilisticMembership,
    possibilistic_membership2: PossibilisticMembership,
    type: FuzzyOr,
    feature: QgsFeature,
    parent: QgsExpression,
):
    if not isinstance(possibilistic_membership1, PossibilisticMembership):
        raise TypeError(prepare_error_message(possibilistic_membership1, "possibilistic_membership1"))

    if not isinstance(possibilistic_membership2, PossibilisticMembership):
        raise TypeError(prepare_error_message(possibilistic_membership2, "possibilistic_membership2"))

    if not (isinstance(type, str) and type in FUZZY_OR_NAMES):
        raise TypeError(prepare_type_error_message(type, FUZZY_OR_NAMES))

    return PossibilisticOr.possibilisticOr(possibilistic_membership1, possibilistic_membership2, type=type)

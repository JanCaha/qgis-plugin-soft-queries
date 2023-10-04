from typing import Any, List, Union

from FuzzyMath import FuzzyAnd, FuzzyMembership, FuzzyOr
from FuzzyMath.class_fuzzy_number import FuzzyNumber
from FuzzyMath.class_membership_operations import (
    FUZZY_AND_NAMES,
    FUZZY_OR_NAMES,
    fuzzyAnds,
    fuzzyOrs,
)
from qgis.core import QgsExpression, QgsFeature, qgsfunction

from ..text_constants import TextConstants
from .qgsexpressions_utils import error_message, load_help


def prepare_error_message(
    object: Any,
    parameter_name: str = "fuzzy_membership",
    class_name: str = "FuzzyMembership",
) -> str:
    return error_message(parameter_name, class_name, object)


def prepare_type_error_message(type_value: str, allowed_values: List[str]) -> str:
    return f"`type` value `{type_value}` is not from allowed values [{', '.join(allowed_values)}]"


@qgsfunction(
    args="auto",
    group=TextConstants.exp_funcs_group,
    helpText=load_help("fuzzy_membership"),
    register=False,
)
def fuzzy_membership(
    value: Union[float, int], feature: QgsFeature, parent: QgsExpression
):
    if isinstance(value, (int, float)):
        return FuzzyMembership(value)

    else:
        raise Exception(prepare_error_message(value, "value", "int, float"))


@qgsfunction(
    args="auto",
    group=TextConstants.exp_funcs_group,
    helpText=load_help("fuzzy_and"),
    register=False,
)
def fuzzy_and(
    fuzzy_membership1: FuzzyMembership,
    fuzzy_membership2: FuzzyMembership,
    type: fuzzyAnds,
    feature: QgsFeature,
    parent: QgsExpression,
):
    if not isinstance(fuzzy_membership1, FuzzyMembership):
        raise Exception(prepare_error_message(fuzzy_membership, "fuzzy_membership1"))

    if not isinstance(fuzzy_membership2, FuzzyMembership):
        raise Exception(prepare_error_message(fuzzy_membership, "fuzzy_membership2"))

    if not (isinstance(type, str) and type in FUZZY_AND_NAMES):
        raise Exception(prepare_type_error_message(type, FUZZY_AND_NAMES))

    return FuzzyAnd.fuzzyAnd(fuzzy_membership1, fuzzy_membership2, type=type)


@qgsfunction(
    args="auto",
    group=TextConstants.exp_funcs_group,
    helpText=load_help("fuzzy_or"),
    register=False,
)
def fuzzy_or(
    fuzzy_membership1: FuzzyMembership,
    fuzzy_membership2: FuzzyMembership,
    type: fuzzyOrs,
    feature: QgsFeature,
    parent: QgsExpression,
):
    if not isinstance(fuzzy_membership1, FuzzyMembership):
        raise Exception(prepare_error_message(fuzzy_membership, "fuzzy_membership1"))

    if not isinstance(fuzzy_membership2, FuzzyMembership):
        raise Exception(prepare_error_message(fuzzy_membership, "fuzzy_membership2"))

    if not (isinstance(type, str) and type in FUZZY_OR_NAMES):
        raise Exception(prepare_type_error_message(type, FUZZY_OR_NAMES))

    return FuzzyOr.fuzzyOr(fuzzy_membership1, fuzzy_membership2, type=type)


@qgsfunction(
    args="auto",
    group=TextConstants.exp_funcs_group,
    helpText=load_help("membership"),
    register=False,
)
def membership(
    fuzzy_membership: FuzzyMembership, feature: QgsFeature, parent: QgsExpression
):
    if isinstance(fuzzy_membership, FuzzyMembership):
        return fuzzy_membership.membership

    else:
        raise Exception(prepare_error_message(fuzzy_membership))


@qgsfunction(
    args="auto",
    group=TextConstants.exp_funcs_group,
    helpText=load_help("calculate_fuzzy_membership"),
    register=False,
)
def calculate_fuzzy_membership(
    value: Union[float, int],
    fn: FuzzyNumber,
    feature: QgsFeature,
    parent: QgsExpression,
):
    if not isinstance(fn, FuzzyNumber):
        raise Exception(prepare_error_message(fn, "fn", "FuzzyNumber"))

    if not isinstance(value, (int, float)):
        raise Exception(prepare_error_message(value, "value", "float, int"))

    return fn.membership(value)

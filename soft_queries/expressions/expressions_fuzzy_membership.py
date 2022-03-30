from qgis.core import (qgsfunction, QgsExpression, QgsFeature)

from ..FuzzyMath import FuzzyMembership, FuzzyAnd, FuzzyOr

from ..text_constants import TextConstants
from ..utils import string_to_python_object, python_object_to_string
from .qgsexpressions_utils import load_help

FUZZY_MEMBERSHIP_STRING = "fuzzy_membership_"


@qgsfunction(args="auto",
             group=TextConstants.exp_funcs_group,
             helpText=load_help("fuzzy_membership_as_text"),
             register=False)
def fuzzy_membership_as_text(fuzzy_membership: FuzzyMembership, feature: QgsFeature,
                             parent: QgsExpression):

    if isinstance(fuzzy_membership, FuzzyMembership):
        return repr(fuzzy_membership)

    else:
        raise Exception("`fuzzy_membership` is not of Python class `FuzzyMembership`.")


@qgsfunction(args="auto",
             group=TextConstants.exp_funcs_group,
             helpText=load_help("fuzzy_membership_to_string_repr"),
             register=False)
def fuzzy_membership_to_string_repr(fuzzy_membership: FuzzyMembership, feature: QgsFeature,
                                    parent: QgsExpression):

    if isinstance(fuzzy_membership, FuzzyMembership):
        return python_object_to_string(fuzzy_membership, FUZZY_MEMBERSHIP_STRING)

    else:
        raise Exception("First argument must be `FuzzyMembership`, it is `{0}`.".format(
            type(fuzzy_membership).__name__))


@qgsfunction(args='auto',
             group=TextConstants.exp_funcs_group,
             helpText=load_help("fuzzy_membership_from_string_repr"),
             register=False)
def fuzzy_membership_from_string_repr(string_fuzzy_membership: FuzzyMembership,
                                      feature: QgsFeature, parent: QgsExpression):

    if isinstance(string_fuzzy_membership,
                  str) and string_fuzzy_membership.startswith(FUZZY_MEMBERSHIP_STRING):
        return string_to_python_object(string_fuzzy_membership, FUZZY_MEMBERSHIP_STRING)

    else:
        raise Exception("First argument must be `str` and start with `{1}`, it is `{0}`.".format(
            type(string_fuzzy_membership).__name__, FUZZY_MEMBERSHIP_STRING))


@qgsfunction(args='auto',
             group=TextConstants.exp_funcs_group,
             helpText=load_help("fuzzy_membership"),
             register=False)
def fuzzy_membership(value, feature: QgsFeature, parent: QgsExpression):

    return FuzzyMembership(value)


@qgsfunction(args="auto",
             group=TextConstants.exp_funcs_group,
             helpText=load_help("fuzzy_and"),
             register=False)
def fuzzy_and(fuzzy_membership1: FuzzyMembership, fuzzy_membership2: FuzzyMembership, type: str,
              feature: QgsFeature, parent: QgsExpression):

    return FuzzyAnd.fuzzyAnd(fuzzy_membership1, fuzzy_membership2, type=type)


@qgsfunction(args="auto",
             group=TextConstants.exp_funcs_group,
             helpText=load_help("fuzzy_or"),
             register=False)
def fuzzy_or(fuzzy_membership1: FuzzyMembership, fuzzy_membership2: FuzzyMembership, type: str,
             feature: QgsFeature, parent: QgsExpression):

    return FuzzyOr.fuzzyOr(fuzzy_membership1, fuzzy_membership2, type=type)


@qgsfunction(args="auto",
             group=TextConstants.exp_funcs_group,
             helpText=load_help("membership"),
             register=False)
def membership(fuzzy_membership: FuzzyMembership, feature: QgsFeature, parent: QgsExpression):

    if isinstance(fuzzy_membership, FuzzyMembership):
        return fuzzy_membership.membership

    else:
        raise Exception(
            "`fuzzy_membership` is not of Python class `FuzzyMembership`. It is `{}`.".format(
                type(fuzzy_membership).__name__))

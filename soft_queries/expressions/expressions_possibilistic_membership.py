from qgis.core import (qgsfunction, QgsExpression, QgsFeature)

from ..FuzzyMath import FuzzyNumber, PossibilisticMembership, PossibilisticAnd, PossibilisticOr

from ..text_constants import TextConstants
from ..utils import string_to_python_object, python_object_to_string
from .qgsexpressions_utils import load_help

POSSIBILISTIC_MEMBERSHIP_STRING = "possibilistic_membership_"


@qgsfunction(args="auto",
             group=TextConstants.exp_funcs_group,
             helpText=load_help("possibilistic_membership_as_text"),
             register=False)
def possibilistic_membership_as_text(possibilistic_membership: PossibilisticMembership,
                                     feature: QgsFeature, parent: QgsExpression):

    if isinstance(possibilistic_membership, PossibilisticMembership) or \
       type(possibilistic_membership).__name__ == "PossibilisticMembership":

        repr_str = repr(possibilistic_membership)

    else:
        raise Exception("First argument must be `PossibilisticMembership`, it is `{0}`.".format(
            type(possibilistic_membership).__name__))

    return repr_str


@qgsfunction(args="auto",
             group=TextConstants.exp_funcs_group,
             helpText=load_help("possibilistic_membership_to_string_repr"),
             register=False)
def possibilistic_membership_to_string_repr(possibilistic_membership: PossibilisticMembership,
                                            feature: QgsFeature, parent: QgsExpression):

    if isinstance(possibilistic_membership, PossibilisticMembership):
        possibilistic_membership_string = python_object_to_string(possibilistic_membership,
                                                                  POSSIBILISTIC_MEMBERSHIP_STRING)

    else:
        raise Exception("First argument must be `PossibilisticMembership`, it is `{0}`.".format(
            type(possibilistic_membership).__name__))

    return possibilistic_membership_string


@qgsfunction(args='auto',
             group=TextConstants.exp_funcs_group,
             helpText=load_help("possibilistic_membership_from_string_repr"),
             register=False)
def possibilistic_membership_from_string_repr(
        string_possibilistic_membership: PossibilisticMembership, feature: QgsFeature,
        parent: QgsExpression):

    if isinstance(
            string_possibilistic_membership,
            str) and string_possibilistic_membership.startswith(POSSIBILISTIC_MEMBERSHIP_STRING):
        pm = string_to_python_object(string_possibilistic_membership,
                                     POSSIBILISTIC_MEMBERSHIP_STRING)

    else:
        raise Exception("First argument must be `str` and start with `{1}`, it is `{0}`.".format(
            type(string_possibilistic_membership).__name__, POSSIBILISTIC_MEMBERSHIP_STRING))

    return pm


@qgsfunction(args='auto',
             group=TextConstants.exp_funcs_group,
             helpText=load_help("possibilistic_membership"),
             register=False)
def possibilistic_membership(possibility, necessity, feature: QgsFeature, parent: QgsExpression):

    pm = PossibilisticMembership(possibility, necessity)

    return pm


@qgsfunction(args="auto",
             group=TextConstants.exp_funcs_group,
             helpText=load_help("possibility"),
             register=False)
def possibility(possibilistic_membership: PossibilisticMembership, feature: QgsFeature,
                parent: QgsExpression):

    if isinstance(possibilistic_membership, PossibilisticMembership):
        return possibilistic_membership.possibility

    else:
        raise Exception(
            "`possibilistic_membership` is not of Python class `PossibilisticMembership`.")


@qgsfunction(args="auto",
             group=TextConstants.exp_funcs_group,
             helpText=load_help("necessity"),
             register=False)
def necessity(possibilistic_membership: PossibilisticMembership, feature: QgsFeature,
              parent: QgsExpression):

    if isinstance(possibilistic_membership, PossibilisticMembership):
        return possibilistic_membership.necessity

    else:
        raise Exception(
            "`possibilistic_membership` is not of Python class `PossibilisticMembership`.")


@qgsfunction(args="auto",
             group=TextConstants.exp_funcs_group,
             helpText=load_help("possibilistic_and"),
             register=False)
def possibilistic_and(possibilistic_membership1: PossibilisticMembership,
                      possibilistic_membership2: PossibilisticMembership, type: str,
                      feature: QgsFeature, parent: QgsExpression):

    return PossibilisticAnd.possibilisticAnd(possibilistic_membership1,
                                             possibilistic_membership2,
                                             type=type)


@qgsfunction(args="auto",
             group=TextConstants.exp_funcs_group,
             helpText=load_help("possibilistic_or"),
             register=False)
def possibilistic_or(possibilistic_membership1: PossibilisticMembership,
                     possibilistic_membership2: PossibilisticMembership, type: str,
                     feature: QgsFeature, parent: QgsExpression):

    return PossibilisticOr.possibilisticOr(possibilistic_membership1,
                                           possibilistic_membership2,
                                           type=type)


@qgsfunction(args="auto",
             group=TextConstants.exp_funcs_group,
             helpText=load_help("possibilistic_exceedance"),
             register=False)
def possibilistic_exceedance(fn_a: FuzzyNumber, fn_b: FuzzyNumber, feature: QgsFeature,
                             parent: QgsExpression):

    if not isinstance(fn_a, FuzzyNumber):
        raise Exception("First argument must be `FuzzyNumber`, it is `{}`.".format(
            type(fn_a).__name__))

    if not isinstance(fn_b, FuzzyNumber):
        raise Exception("Second argument must be `FuzzyNumber`, it is `{}`.".format(
            type(fn_b).__name__))

    return fn_a.exceedance(fn_b)


@qgsfunction(args="auto",
             group=TextConstants.exp_funcs_group,
             helpText=load_help("possibilistic_undervaluation"),
             register=False)
def possibilistic_undervaluation(fn_a: FuzzyNumber, fn_b: FuzzyNumber, feature: QgsFeature,
                                 parent: QgsExpression):

    if not isinstance(fn_a, FuzzyNumber):
        raise Exception("First argument must be `FuzzyNumber`, it is `{}`.".format(
            type(fn_a).__name__))

    if not isinstance(fn_b, FuzzyNumber):
        raise Exception("Second argument must be `FuzzyNumber`, it is `{}`.".format(
            type(fn_b).__name__))

    return fn_a.undervaluation(fn_b)


@qgsfunction(args="auto",
             group=TextConstants.exp_funcs_group,
             helpText=load_help("possibilistic_strict_exceedance"),
             register=False)
def possibilistic_strict_exceedance(fn_a: FuzzyNumber, fn_b: FuzzyNumber, feature: QgsFeature,
                                    parent: QgsExpression):

    if not isinstance(fn_a, FuzzyNumber):
        raise Exception("First argument must be `FuzzyNumber`, it is `{}`.".format(
            type(fn_a).__name__))

    if not isinstance(fn_b, FuzzyNumber):
        raise Exception("Second argument must be `FuzzyNumber`, it is `{}`.".format(
            type(fn_b).__name__))

    return fn_a.strict_exceedance(fn_b)


@qgsfunction(args="auto",
             group=TextConstants.exp_funcs_group,
             helpText=load_help("possibilistic_strict_undervaluation"),
             register=False)
def possibilistic_strict_undervaluation(fn_a: FuzzyNumber, fn_b: FuzzyNumber, feature: QgsFeature,
                                        parent: QgsExpression):

    if not isinstance(fn_a, FuzzyNumber):
        raise Exception("First argument must be `FuzzyNumber`, it is `{}`.".format(
            type(fn_a).__name__))

    if not isinstance(fn_b, FuzzyNumber):
        raise Exception("Second argument must be `FuzzyNumber`, it is `{}`.".format(
            type(fn_b).__name__))

    return fn_a.strict_undervaluation(fn_b)

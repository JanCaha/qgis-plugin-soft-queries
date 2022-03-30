from qgis.core import (qgsfunction, QgsExpression, QgsFeature)

from qgis.PyQt.QtCore import QVariant

from ..FuzzyMath import FuzzyNumberFactory, FuzzyNumber

from ..text_constants import TextConstants
from .qgsexpressions_utils import load_help
from ..database.class_db import FuzzyDatabase
from ..utils import string_to_python_object, python_object_to_string

FUZZY_NUMBER_STRING = "fuzzy_number_"


@qgsfunction(args="auto",
             group=TextConstants.exp_funcs_group,
             helpText=load_help("fuzzy_number_triangular"),
             register=False)
def fuzzy_number_triangular(min: float, kernel: float, max: float, feature: QgsFeature,
                            parent: QgsExpression):

    if not isinstance(min, (int, float)):
        raise Exception("`min` should be `int` or `float` but it is `{}`.".format(
            type(min).__name__))

    if not isinstance(kernel, (int, float)):
        raise Exception("`kernel` should be `int` or `float` but it is `{}`.".format(
            type(kernel).__name__))

    if not isinstance(max, (int, float)):
        raise Exception("`max` should be `int` or `float` but it is `{}`.".format(
            type(max).__name__))

    return FuzzyNumberFactory.triangular(min, kernel, max)


@qgsfunction(args="auto",
             group=TextConstants.exp_funcs_group,
             helpText=load_help("fuzzy_number_trapezoidal"),
             register=False)
def fuzzy_number_trapezoidal(min: float, kernel_min: float, kernel_max: float, max: float,
                             feature: QgsFeature, parent: QgsExpression):

    if not isinstance(min, (int, float)):
        raise Exception("`min` should be `int` or `float` but it is `{}`.".format(
            type(min).__name__))

    if not isinstance(kernel_min, (int, float)):
        raise Exception("`kernel_min` should be `int` or `float` but it is `{}`.".format(
            type(kernel_min).__name__))

    if not isinstance(kernel_max, (int, float)):
        raise Exception("`kernel_max` should be `int` or `float` but it is `{}`.".format(
            type(kernel_max).__name__))

    if not isinstance(max, (int, float)):
        raise Exception("`max` should be `int` or `float` but it is `{}`.".format(
            type(max).__name__))

    return FuzzyNumberFactory.trapezoidal(min, kernel_min, kernel_max, max)


@qgsfunction(args="auto",
             group=TextConstants.exp_funcs_group,
             helpText=load_help("get_fuzzy_number_from_db"),
             register=False)
def get_fuzzy_number_from_db(name: str, feature: QgsFeature, parent: QgsExpression):

    fdb = FuzzyDatabase()

    fn = fdb.get_fuzzy_variable(name)

    return fn


@qgsfunction(args="auto",
             group=TextConstants.exp_funcs_group,
             helpText=load_help("fuzzy_number_to_string_repr"),
             register=False)
def fuzzy_number_to_string_repr(fuzzy: FuzzyNumber, feature: QgsFeature, parent: QgsExpression):

    if isinstance(fuzzy, FuzzyNumber):
        fn_string = python_object_to_string(fuzzy, FUZZY_NUMBER_STRING)

    return fn_string


@qgsfunction(args='auto',
             group=TextConstants.exp_funcs_group,
             helpText=load_help("fuzzy_number_from_string_repr"),
             register=False)
def fuzzy_number_from_string_repr(value: str, feature: QgsFeature, parent: QgsExpression):

    if isinstance(value, str) and value.startswith(FUZZY_NUMBER_STRING):
        fn = string_to_python_object(value, FUZZY_NUMBER_STRING)

    return fn


@qgsfunction(args='auto',
             group=TextConstants.exp_funcs_group,
             helpText=load_help("fuzzy_number_as_text"),
             register=False)
def fuzzy_number_as_text(fn: FuzzyNumber, feature: QgsFeature, parent: QgsExpression):

    if isinstance(fn, FuzzyNumber):
        return str(fn)

    else:
        return None

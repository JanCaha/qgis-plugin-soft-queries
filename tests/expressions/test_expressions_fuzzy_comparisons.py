import pytest

from soft_queries.FuzzyMath import PossibilisticMembership

from qgis.core import QgsExpression

from . import assert_has_error, assert_is_correct


@pytest.mark.parametrize("params", [
    "1, 1",
    "0.5, 0.5",
    "fuzzy_number_triangular(1,2,3), fuzzy_number_triangular(2,3,4)",
])
def test_validate_inputs_convert_fns(params):

    exp = QgsExpression(f"possibilistic_exceedance({params})")

    assert_is_correct(exp, PossibilisticMembership)


@pytest.mark.parametrize("params, msg", [
    ("'a', 1", "`fn_1` parameter"),
    ("0.5, 'a'", "`fn_2` parameter"),
])
def test_validate_inputs_convert_fns_errors(params, msg):

    exp = QgsExpression(f"possibilistic_exceedance({params})")

    assert_has_error(exp, msg)


@pytest.mark.parametrize("params, exp", [
    ("fuzzy_number_triangular(1,2,3), fuzzy_number_triangular(2,3,4)", "possibilistic_exceedance"),
    ("fuzzy_number_triangular(1,2,3), fuzzy_number_triangular(2,3,4)",
     "possibilistic_undervaluation"),
    ("fuzzy_number_triangular(1,2,3), fuzzy_number_triangular(2,3,4)",
     "possibilistic_strict_exceedance"),
    ("fuzzy_number_triangular(1,2,3), fuzzy_number_triangular(2,3,4)",
     "possibilistic_strict_undervaluation"),
])
def test_comparisons(params, exp):

    exp = QgsExpression(f"{exp}({params})")

    assert_is_correct(exp, PossibilisticMembership)
    
import pytest

from qgis.core import QgsExpression

from soft_queries.FuzzyMath import PossibilisticMembership

from . import assert_is_correct, assert_has_error


def test_expr_possibilistic_membership():

    exp = QgsExpression("possibilistic_membership(0.5, 0.3)")

    assert_is_correct(exp, PossibilisticMembership, PossibilisticMembership(0.5, 0.3))


@pytest.mark.parametrize("exp_params, msg", [
    ("'a', 0.5", "`possibility` parameter"),
    ("0.5, 'a'", "`necessity` parameter"),
])
def test_expr_possibilistic_membership_erros(exp_params, msg):

    exp = QgsExpression(f"possibilistic_membership({exp_params})")

    assert_has_error(exp, msg)


def test_expr_possibilistic_membership_as_text():

    exp = QgsExpression("sq_as_string(possibilistic_membership(0.5, 0.3))")

    str_repr = "PossibilisticMembership(possibility: 0.5, necessity: 0.3)"

    assert_is_correct(exp, str, str_repr)


def test_expr_possibilistic_membership_as_text_errors():

    exp = QgsExpression("sq_as_string('a')")

    assert_has_error(exp, "Parameter `sq_object`")


def test_expr_possibilistic_membership_to_string_repr():

    exp = QgsExpression("sq_to_string_repr(possibilistic_membership(0.5, 0.3))")

    str_repr = "possibilistic_membership_gASVgQAAAAAAAACMKHNvZnRfcXVlcmllcy5GdXp6eU1hdGguY2xhc3NfbWVtYmVyc2hpcHOUjBdQ\nb3NzaWJpbGlzdGljTWVtYmVyc2hpcJSTlCmBlE59lCiMDF9wb3NzaWJpbGl0eZRHP+AAAAAAAACM\nCl9uZWNlc3NpdHmURz/TMzMzMzMzdYaUYi4=\n"

    assert_is_correct(exp, str, str_repr)


def test_expr_possibilistic_membership_to_string_repr_errors():

    exp = QgsExpression("sq_to_string_repr(0.5)")

    assert_has_error(exp, "Parameter `sq_object`")


def test_expr_possibilistic_membership_from_string_repr():

    str_repr = "possibilistic_membership_gASVgQAAAAAAAACMKHNvZnRfcXVlcmllcy5GdXp6eU1hdGguY2xhc3NfbWVtYmVyc2hpcHOUjBdQb3NzaWJpbGlzdGljTWVtYmVyc2hpcJSTlCmBlE59lCiMDF9wb3NzaWJpbGl0eZRHP+AAAAAAAACMCl9uZWNlc3NpdHmURz/TMzMzMzMzdYaUYi4="

    exp = QgsExpression(f"sq_from_string_repr('{str_repr}')")

    assert_is_correct(exp, PossibilisticMembership, PossibilisticMembership(0.5, 0.3))


def test_expr_possibilistic_membership_from_string_repr_errors():

    exp = QgsExpression("sq_from_string_repr('a')")

    assert_has_error(exp, "Parameter `str \(with correct prefix\)`")


def test_expr_possibility():

    exp = QgsExpression("possibility(possibilistic_membership(0.5, 0.3))")

    assert_is_correct(exp, float, 0.5)


def test_expr_possibility_errors():

    exp = QgsExpression("possibility(0.5)")

    assert_has_error(exp, "`possibilistic_membership`")


def test_expr_necessity():

    exp = QgsExpression("necessity(possibilistic_membership(0.5, 0.3))")

    assert_is_correct(exp, float, 0.3)


def test_expr_necessity_errors():

    exp = QgsExpression("necessity(0.5)")

    assert_has_error(exp, "`possibilistic_membership`")


def test_expr_possibilistic_and():

    exp = QgsExpression(
        "possibilistic_and(possibilistic_membership(0.5, 0.3), possibilistic_membership(0.7, 0.15), 'min')"
    )

    assert_is_correct(exp, PossibilisticMembership, PossibilisticMembership(0.5, 0.15))


@pytest.mark.parametrize("exp_params, type, msg", [
    ("0.5, possibilistic_membership(0.5, 0.3)", "min", "`possibilistic_membership1` parameter"),
    ("possibilistic_membership(0.5, 0.3), 0.75", "min", "`possibilistic_membership2` parameter"),
    ("possibilistic_membership(0.5, 0.3), possibilistic_membership(0.5, 0.3)",
     "non_existing_operation_type", "`type` value `non_existing_operation_type`"),
])
def test_expr_possibilistic_and_errors(exp_params, type, msg):

    exp = QgsExpression(f"possibilistic_and({exp_params}, '{type}')")

    assert_has_error(exp, msg)


def test_expr_possibilistic_or():

    exp = QgsExpression(
        "possibilistic_or(possibilistic_membership(0.5, 0.3), possibilistic_membership(0.7, 0.15), 'max')"
    )

    assert_is_correct(exp, PossibilisticMembership, PossibilisticMembership(0.7, 0.3))


@pytest.mark.parametrize("exp_params, type, msg", [
    ("0.5, possibilistic_membership(0.5, 0.3)", "max", "`possibilistic_membership1` parameter"),
    ("possibilistic_membership(0.5, 0.3), 0.75", "max", "`possibilistic_membership2` parameter"),
    ("possibilistic_membership(0.5, 0.3), possibilistic_membership(0.5, 0.3)",
     "non_existing_operation_type", "`type` value `non_existing_operation_type`"),
])
def test_expr_possibilistic_or_errors(exp_params, type, msg):

    exp = QgsExpression(f"possibilistic_or({exp_params}, '{type}')")

    assert_has_error(exp, msg)

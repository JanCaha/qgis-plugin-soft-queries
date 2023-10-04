import pytest
from qgis.core import QgsExpression

from soft_queries.FuzzyMath import FuzzyMembership

from . import assert_has_error, assert_is_correct


def test_expr_fuzzy_membership():

    exp = QgsExpression("fuzzy_membership(0.5)")

    assert_is_correct(exp, FuzzyMembership, FuzzyMembership(0.5))


@pytest.mark.parametrize(
    "exp",
    [
        "fuzzy_membership('a')",
    ],
)
def test_expr_fuzzy_membership_error(exp):

    exp = QgsExpression(exp)

    assert_has_error(exp, "`value` parameter is not of Python class `int, float`")


def test_expr_fuzzy_membership_as_text():

    exp = QgsExpression("sq_as_string(fuzzy_membership(0.5))")

    assert_is_correct(exp, str, "FuzzyMembership(0.5)")


def test_expr_fuzzy_membership_as_text_errors():

    exp = QgsExpression("sq_as_string('a')")

    assert_has_error(exp, "Parameter `sq_object`")


def test_expr_fuzzy_membership_to_string_repr():

    exp = QgsExpression("sq_to_string_repr(fuzzy_membership(0.5))")

    text_rep = "fuzzy_membership_gASVYQAAAAAAAACMKHNvZnRfcXVlcmllcy5GdXp6eU1hdGguY2xhc3NfbWVtYmVyc2hpcHOUjA9G\ndXp6eU1lbWJlcnNoaXCUk5QpgZROfZSMC19tZW1iZXJzaGlwlEc/4AAAAAAAAHOGlGIu\n"

    assert_is_correct(exp, str, text_rep)


@pytest.mark.parametrize(
    "exp",
    [
        "sq_to_string_repr(1)",
        "sq_to_string_repr('a')",
    ],
)
def test_expr_fuzzy_membership_to_string_repr_errors(exp):

    exp = QgsExpression(exp)

    assert_has_error(exp, "Parameter `sq_object`")


def test_expr_fuzzy_membership_from_string_repr():

    text_rep = "fuzzy_membership_gASVYQAAAAAAAACMKHNvZnRfcXVlcmllcy5GdXp6eU1hdGguY2xhc3NfbWVtYmVyc2hpcHOUjA9GdXp6eU1lbWJlcnNoaXCUk5QpgZROfZSMC19tZW1iZXJzaGlwlEc/4AAAAAAAAHOGlGIu"

    exp = QgsExpression(f"sq_from_string_repr('{text_rep}')")

    assert_is_correct(exp, FuzzyMembership, FuzzyMembership(0.5))


def test_expr_fuzzy_membership_from_string_repr_errors():

    text_rep = "gASVYQAAAAAAAACMKHNvZnRfcXVlcmllcy5GdXp6eU1hdGguY2xhc3NfbWVtYmVyc2hpcHOUjA9GdXp6eU1lbWJlcnNoaXCUk5QpgZROfZSMC19tZW1iZXJzaGlwlEc/4AAAAAAAAHOGlGIu"

    exp = QgsExpression(f"sq_from_string_repr('{text_rep}')")

    assert_has_error(exp, "Parameter `str \(with correct prefix\)`")

    exp = QgsExpression("sq_from_string_repr(1)")

    assert_has_error(exp, "Parameter `str \(with correct prefix\)`")


def test_expr_membership():

    exp = QgsExpression("membership(fuzzy_membership(0.5))")

    assert_is_correct(exp, float, 0.5)


def test_expr_membership_errors():

    exp = QgsExpression("membership(0.5)")

    assert_has_error(
        exp, "`fuzzy_membership` parameter is not of Python class `FuzzyMembership`"
    )


def test_expr_fuzzy_and():

    exp = QgsExpression(
        "fuzzy_and(fuzzy_membership(0.5), fuzzy_membership(0.75), 'min')"
    )

    assert_is_correct(exp, FuzzyMembership, FuzzyMembership(0.5))


@pytest.mark.parametrize(
    "exp_params, type, msg",
    [
        ("0.5, fuzzy_membership(0.75)", "min", "`fuzzy_membership1` parameter"),
        ("fuzzy_membership(0.5), 0.75", "min", "`fuzzy_membership2` parameter"),
        (
            "fuzzy_membership(0.5), fuzzy_membership(0.5)",
            "non_existing_operation_type",
            "`type` value `non_existing_operation_type`",
        ),
    ],
)
def test_expr_fuzzy_and_errors(exp_params, type, msg):

    exp = QgsExpression(f"fuzzy_and({exp_params}, '{type}')")

    assert_has_error(exp, msg)


def test_expr_fuzzy_or():

    exp = QgsExpression(
        "fuzzy_or(fuzzy_membership(0.5), fuzzy_membership(0.75), 'max')"
    )

    assert_is_correct(exp, FuzzyMembership, FuzzyMembership(0.75))


@pytest.mark.parametrize(
    "exp_params, type, msg",
    [
        ("0.5, fuzzy_membership(0.75)", "max", "`fuzzy_membership1` parameter"),
        ("fuzzy_membership(0.5), 0.75", "max", "`fuzzy_membership2` parameter"),
        (
            "fuzzy_membership(0.5), fuzzy_membership(0.5)",
            "non_existing_operation_type",
            "`type` value `non_existing_operation_type`",
        ),
    ],
)
def test_expr_fuzzy_or_errors(exp_params, type, msg):

    exp = QgsExpression(f"fuzzy_or({exp_params}, '{type}')")

    assert_has_error(exp, msg)


def test_calculate_fuzzy_membership():

    exp = QgsExpression(
        "calculate_fuzzy_membership(1.5, fuzzy_number_triangular(1,2,3))"
    )

    assert_is_correct(exp, FuzzyMembership, FuzzyMembership(0.5))


@pytest.mark.parametrize(
    "exp_params, msg",
    [
        (
            "'a', fuzzy_number_triangular(1,2,3)",
            "`value` parameter is not of Python class `float, int`",
        ),
        ("1, 0.75", "`fn` parameter is not of Python class `FuzzyNumber`"),
    ],
)
def test_calculate_fuzzy_membership_errors(exp_params, msg):

    exp = QgsExpression(f"calculate_fuzzy_membership({exp_params})")

    assert_has_error(exp, msg)

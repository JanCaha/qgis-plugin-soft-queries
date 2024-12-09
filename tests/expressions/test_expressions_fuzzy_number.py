import pytest
from FuzzyMath import FuzzyNumber, FuzzyNumberFactory
from qgis.core import QgsExpression

from tests.assert_helpers import assert_has_error, assert_is_correct, assert_is_empty


@pytest.mark.parametrize(
    "exp",
    [
        "fuzzy_number_triangular(1,2,3)",
        "fuzzy_number_triangular(1.0,2.0,3.0)",
        "fuzzy_number_triangular(1,2.0,3.9)",
    ],
)
def test_exp_fuzzy_number_triangular(exp):
    exp = QgsExpression(exp)

    assert_is_correct(exp, FuzzyNumber)


@pytest.mark.parametrize(
    "exp, msg",
    [
        (
            "fuzzy_number_triangular(1,2,3,4)",
            "got multiple values for argument",
        ),
        ("fuzzy_number_triangular('a',2,3)", "`min`"),
        ("fuzzy_number_triangular(2,'a',3)", "`kernel`"),
        ("fuzzy_number_triangular(2,3,'a')", "`max`"),
    ],
)
def test_exp_fuzzy_number_triangular_errors(exp, msg):
    exp = QgsExpression(exp)

    assert_has_error(exp, msg)


@pytest.mark.parametrize(
    "exp",
    [
        "fuzzy_number_trapezoidal(1,2,3,4)",
        "fuzzy_number_trapezoidal(1.0,2.0,3.0,4.0)",
        "fuzzy_number_trapezoidal(1,2.0,3.9,4)",
    ],
)
def test_exp_fuzzy_number_trapezoidal(exp):
    exp = QgsExpression(exp)

    result = exp.evaluate()

    assert isinstance(result, FuzzyNumber)

    assert_is_correct(exp)


@pytest.mark.parametrize(
    "exp, msg",
    [
        (
            "fuzzy_number_trapezoidal(1,2,3)",
            "missing 1 required positional argument",
        ),
        ("fuzzy_number_trapezoidal('a',2,3,4)", "`min`"),
        ("fuzzy_number_trapezoidal(2,'a',3,4)", "`kernel_min`"),
        ("fuzzy_number_trapezoidal(2,3,'a',4)", "`kernel_max`"),
        ("fuzzy_number_trapezoidal(2,3,4,'a')", "`max`"),
    ],
)
def test_exp_fuzzy_number_trapezoidal_errors(exp, msg):
    exp = QgsExpression(exp)

    assert_has_error(exp, msg)


def test_exp_fuzzy_number_to_string_repr():
    exp = QgsExpression("sq_to_string_repr(fuzzy_number_trapezoidal(1,2,3,4))")

    text_rep = "fuzzy_number_gASVAgEAAAAAAACMHEZ1enp5TWF0aC5jbGFzc19mdXp6eV9udW1iZXKUjAtGdXp6eU51bWJlcpST\nlCmBlE59lCiMC19hbHBoYV9jdXRzlH2UKEsAjBhGdXp6eU1hdGguY2xhc3NfaW50ZXJ2YWyUjAhJ\nbnRlcnZhbJSTlCmBlE59lCiMBF9taW6URz/wAAAAAAAAjARfbWF4lEdAEAAAAAAAAIwKX3ByZWNp\nc2lvbpRLD4wLX2RlZ2VuZXJhdGWUiXWGlGJLAWgJKYGUTn2UKGgMR0AAAAAAAAAAaA1HQAgAAAAA\nAABoDksPaA+JdYaUYnWMB19hbHBoYXOUXZQoSwBLAWVoDksPdYaUYi4=\n"
    assert_is_correct(exp, str, text_rep)


@pytest.mark.parametrize(
    "exp",
    [
        "sq_to_string_repr(1)",
        "sq_to_string_repr('a')",
    ],
)
def test_exp_fuzzy_number_to_string_repr_error(exp):
    exp = QgsExpression(exp)

    assert_has_error(exp)


def test_exp_fuzzy_number_from_string_repr():
    text_rep = "fuzzy_number_gASVAgEAAAAAAACMHEZ1enp5TWF0aC5jbGFzc19mdXp6eV9udW1iZXKUjAtGdXp6eU51bWJlcpST\nlCmBlE59lCiMC19hbHBoYV9jdXRzlH2UKEsAjBhGdXp6eU1hdGguY2xhc3NfaW50ZXJ2YWyUjAhJ\nbnRlcnZhbJSTlCmBlE59lCiMBF9taW6URz/wAAAAAAAAjARfbWF4lEdACAAAAAAAAIwKX3ByZWNp\nc2lvbpRLD4wLX2RlZ2VuZXJhdGWUiXWGlGJLAWgJKYGUTn2UKGgMR0AAAAAAAAAAaA1HQAAAAAAA\nAABoDksPaA+IdYaUYnWMB19hbHBoYXOUXZQoSwBLAWVoDksPdYaUYi4=\n"

    exp = QgsExpression(f"sq_from_string_repr('{text_rep}')")

    assert_is_correct(exp, FuzzyNumber, FuzzyNumberFactory.triangular(1, 2, 3))


@pytest.mark.parametrize(
    "exp",
    [
        "sq_from_string_repr(1)",
        "sq_from_string_repr('a')",
    ],
)
def test_exp_fuzzy_number_from_string_repr_error(exp):
    exp = QgsExpression(exp)

    assert_has_error(exp)


def test_exp_get_fuzzy_number_from_db():
    # exp = QgsExpression("get_fuzzy_number_from_db('a')")

    # assert_is_correct(exp, FuzzyNumber)

    exp = QgsExpression("get_fuzzy_number_from_db('non_existing_record')")

    assert_is_empty(exp)


def test_exp_fuzzy_number_as_text():
    exp = QgsExpression("sq_as_string(fuzzy_number_triangular(1,2,3))")

    assert_is_correct(
        exp,
        str,
        "Fuzzy number with support (1.0,3.0), kernel (2.0, 2.0) and 0 more alpha-cuts.",
    )


@pytest.mark.parametrize(
    "exp",
    [
        "sq_as_string(1)",
        "sq_as_string('a')",
    ],
)
def test_exp_fuzzy_number_as_text_error(exp):
    exp = QgsExpression(exp)

    assert_has_error(exp, "Parameter `sq_object`")

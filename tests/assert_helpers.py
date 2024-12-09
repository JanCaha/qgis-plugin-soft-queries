import re
from typing import Any

from qgis.core import QgsExpression


def assert_is_correct(expression: QgsExpression, result_class: type = None, value: Any = None) -> None:

    __tracebackhide__ = True

    result = expression.evaluate()

    if result_class:
        assert isinstance(
            result, result_class
        ), f"Result should be `{result_class.__name__}` but is `{type(result).__name__}`."

    assert expression.hasEvalError() is False, f"`{expression.expression()}` has eval error."

    assert (
        expression.evalErrorString() == ""
    ), f"`{expression.expression()}` has error string `{expression.evalErrorString()}`."

    if value:
        assert value == result, f"`{value}` != `{result}`."


def extract_error_string(expression: QgsExpression) -> str:

    error_msg = ""

    errors = expression.parserErrors()

    if 0 < len(errors):

        error_msg = errors[0].errorMsg

    else:

        error_msg = expression.evalErrorString()

    return error_msg


def assert_has_error(expression: QgsExpression, error_message: str = None) -> None:

    __tracebackhide__ = True

    result = expression.evaluate()

    assert result is None, f"`{expression.expression()}` has return value but it should be empty."

    assert expression.hasEvalError() is True, f"`{expression.expression()}` does not have eval error."

    if error_message:

        true_error = extract_error_string(expression)

        assert re.search(error_message, true_error), f"`{error_message}` not found in `{true_error}`."


def assert_is_empty(expression: QgsExpression) -> None:

    __tracebackhide__ = True

    result = expression.evaluate()

    assert result is None, f"`{expression.expression()}` has return value but it should be empty."

    assert expression.hasEvalError() is False, f"`{expression.expression()}` has an eval error."

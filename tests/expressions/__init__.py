import re
from typing import Any

import pytest
from qgis.core import QgsExpression


def extract_error_string(expression: QgsExpression) -> str:

    error_msg = ""

    errors = expression.parserErrors()

    if 0 < len(errors):

        error_msg = errors[0].errorMsg

    else:

        error_msg = expression.evalErrorString()

    return error_msg


def assert_is_correct(
    expression: QgsExpression, result_class: type = None, value: Any = None
) -> None:

    __tracebackhide__ = True

    result = expression.evaluate()

    if result_class:
        if not isinstance(result, result_class):
            pytest.fail(
                f"Result should be `{result_class.__name__}` but is `{type(result).__name__}`."
            )

    if expression.hasEvalError():
        pytest.fail(f"`{expression.expression()}` has eval error.")

    if expression.evalErrorString() != "":
        pytest.fail(
            f"`{expression.expression()}` has error string `{expression.evalErrorString()}`."
        )

    if value:
        if not value == result:
            pytest.fail(f"`{value}` != `{result}`")


def assert_has_error(expression: QgsExpression, error_message: str = None) -> None:

    __tracebackhide__ = True

    result = expression.evaluate()

    if result:
        pytest.fail(
            f"`{expression.expression()}` has return value but it should be empty."
        )

    if not expression.hasEvalError():
        pytest.fail(f"`{expression.expression()}` does not have eval error.")

    if error_message:

        true_error = extract_error_string(expression)

        if not re.search(error_message, true_error):
            pytest.fail(f"`{error_message}` not found in `{true_error}`.")


def assert_is_empty(expression: QgsExpression) -> None:

    __tracebackhide__ = True

    result = expression.evaluate()

    if result:
        pytest.fail(
            f"`{expression.expression()}` has return value but it should be empty."
        )

    if expression.hasEvalError():
        pytest.fail(f"`{expression.expression()}` has an eval error.")

from typing import Any
from pathlib import Path


def load_help(function_name: str) -> str:

    path = Path(__file__).parent / "help_files" / "{}.html".format(function_name)

    with open(path) as file:
        help = file.read()

    return help


def error_message(parameter_name: str, class_name: str, object: Any) -> str:
    return "`{}` parameter is not of Python class `{}`. It is `{}`.".\
        format(parameter_name, class_name, type(object).__name__)

from pathlib import Path
from typing import Any


def load_help(function_name: str) -> str:

    path = Path(__file__).parent / "help_files" / "{}.html".format(function_name)

    help_text = ""

    if path.exists():

        with open(path, encoding="utf-8") as file:
            help_text = file.read()

    return help_text


def error_message(parameter_name: str, class_name: str, object: Any) -> str:
    return f"`{parameter_name}` parameter is not of Python class `{class_name}`. It is `{type(object).__name__}`."

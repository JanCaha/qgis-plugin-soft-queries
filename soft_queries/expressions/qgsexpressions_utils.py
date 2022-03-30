from pathlib import Path


def load_help(function_name: str) -> str:

    path = Path(__file__).parent / "help_files" / "{}.html".format(function_name)

    with open(path) as file:
        help = file.read()

    return help

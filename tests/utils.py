from pathlib import Path


def data_path(file_name: str) -> str:
    path = Path(__file__).parent / "_data" / file_name

    return path.as_posix()

import codecs
import os
import pickle
import sys
from pathlib import Path
from typing import Any, Optional

from qgis.core import Qgis, QgsMessageLog

from .text_constants import TextConstants

LOG_DEV = False

if os.environ.get(TextConstants.plugin_dev_env_var):
    if os.environ.get(TextConstants.plugin_dev_env_var).lower() == "true":
        LOG_DEV = True


def get_icons_folder() -> Path:
    return Path(__file__).parent / "icons"


def get_icon_path(file_name: str) -> str:

    file: Path = get_icons_folder() / file_name

    return file.absolute().as_posix()


def log(text: Any) -> None:

    if LOG_DEV:
        QgsMessageLog.logMessage(str(text), TextConstants.plugin_name, Qgis.Info)


def python_object_to_string(object: Any, prefix: Optional[str] = None) -> str:

    object_string = codecs.encode(pickle.dumps(object), "base64").decode()

    if prefix:
        object_string = "{}{}".format(prefix, object_string)

    return object_string


def string_to_python_object(object_string: str, prefix: Optional[str] = None) -> Any:

    if prefix:

        if not object_string.startswith(prefix):
            raise ValueError("Object string does not start with the prefix.")

        object_string = object_string.replace(prefix, "", 1)

    unpickled = pickle.loads(codecs.decode(object_string.encode(), "base64"))

    if unpickled:

        return unpickled

    else:

        return None


def add_deps_folder_to_path() -> None:
    try:
        import FuzzyMath
    except ModuleNotFoundError:
        this_dir = Path(__file__).parent
        deps_dir = this_dir / "deps"
        if deps_dir.exists():
            for f in deps_dir.iterdir():
                sys.path.append(f.as_posix())

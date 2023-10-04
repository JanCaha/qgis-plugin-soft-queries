__author__ = "Jan Caha"
__date__ = "2022-03-01"
__copyright__ = "(C) 2022 by Jan Caha"

import sys
from pathlib import Path

from .plugin_soft_queries import SoftQueriesPlugin

try:
    import FuzzyMath
except ModuleNotFoundError:
    # if required modules are not available on system, let's use the versions that we package
    this_dir = Path(__file__).parent
    deps_dir = this_dir / "deps"
    if deps_dir.exists():
        for f in deps_dir.iterdir():
            sys.path.append(f.as_posix())


# noinspection PyPep8Naming
def classFactory(iface):
    return SoftQueriesPlugin(iface)

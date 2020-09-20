# context.py
import os
import sys

PACKAGE_PARENT = ".."
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
)  # isort:skip # noqa # pylint: disable=wrong-import-position
sys.path.append(
    os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT))
)  # isort: skip # noqa # pylint: disable=wrong-import-position

from src import (  # type: ignore # isort:skip # noqa # pylint: disable=unused-import, wrong-import-position
    person,
)

from src.resources import (  # type: ignore # isort:skip # noqa # pylint: disable=unused-import, wrong-import-position
    constants,
    helpers,
)
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Database wrapper for mops instances."""
import os
import sys
from typing import Optional

PACKAGE_PARENT = ".."
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
)  # isort:skip # noqa # pylint: disable=wrong-import-position
sys.path.append(
    os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT))
)  # isort: skip # noqa # pylint: disable=wrong-import-position

import tinydb  # type: ignore # isort: skip # noqa # pylint: disable=wrong-import-position


class Mops_TinyDB():
    """Wrapper class for TinyDB."""

    def __init__(self, db_path):
        """Connect to DB."""
        self._db = tinydb.TinyDB(db_path + "mops_db.json")

    def add_mop(self, mop: dict) -> int:
        """Add a mop dict to DB."""
        mop_id = self._db.insert(mop)
        mop['id'] = mop_id
        self._db.update(mop, doc_ids=[mop_id])
        return mop_id

    def get_mop(self, mop_id: int) -> Optional[dict]:
        """Return a mop dict with matching id."""
        if self._db.contains(doc_id=mop_id):
            return self._db.get(doc_id=mop_id)
        else:
            return None

    def list_mops(self, field=None, value=None):  # type (str) -> list[dict]
        """Return list of mops."""
        if field is None:
            return self._db.all()
        else:
            return self._db.search(tinydb.where(field) == value)

    def count(self) -> int:
        """Return number of mops in DB."""
        return len(self._db)

    def update(self, mop_id: int, mop: dict) -> None:
        """Modify mop in DB with given mop_id."""
        self._db.update(mop, doc_id=[mop_id])

    def delete(self, mop_id: int) -> None:
        """Remove a mop from DB with given mop_id."""
        self._db.remove(doc_id=[mop_id])

    def delete_all(self):
        """Remove all mops from DB."""
        self._db.truncate()

    def unique_id(self):  # type () -> int
        """Return an integer that does not exist in the db."""
        i = 1
        while self._db.contains(doc_id=[i]):
            i += 1
        return i

    def stop_mops_db(self):
        """Disconnect from DB."""
        pass


def start_mops_db(db_path: str) -> Mops_TinyDB:
    """Connect to DB."""
    return Mops_TinyDB(db_path)

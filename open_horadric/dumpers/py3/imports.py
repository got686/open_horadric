from __future__ import annotations

import enum

from open_horadric.dumpers.base.imports import BaseImport
from open_horadric.dumpers.base.imports import BaseImports


class Imports(BaseImports):
    pass


class Import(BaseImport):
    class Type(enum.IntEnum):
        UNKNOWN = 0
        FUTURE = 1
        CORE = 2
        LIBRARY = 3
        LOCAL = 4

    def __str__(self):
        parts = []
        if self._import_from:
            parts.append("from {}".format(self._import_from))

        parts.append("import {}".format(self._import_name))

        if self._import_as:
            parts.append("as {}".format(self._import_as))

        return " ".join(parts)

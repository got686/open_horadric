from __future__ import annotations

import enum

from open_horadric.dumpers.base.imports import BaseImport
from open_horadric.dumpers.base.imports import BaseImports


class Imports(BaseImports):
    pass


class Exports(BaseImports):
    pass


class Import(BaseImport):
    class Type(enum.IntEnum):
        UNKNOWN = 0
        FUTURE = 1
        CORE = 2
        LIBRARY = 3
        LOCAL = 4

    keyword = "import"

    def __init__(
        self, type_: enum.IntEnum, import_name: str = "", import_from: str = "", import_as: str = "", import_default: str = ""
    ):
        super().__init__(type_, import_name=import_name, import_from=import_from, import_as=import_as)
        self.import_default = import_default

    def __str__(self):
        parts = [self.keyword]

        if self.import_default and self._import_name:
            parts.append("{},".format(self.import_default))
        elif self.import_default:
            parts.append(self.import_default)

        if self._import_name == "*":
            parts.append("*")
        elif self._import_name:
            parts.append("{{ {} }}".format(self._import_name))

        if self._import_as:
            parts.append("as {}".format(self._import_as))

        if self._import_from:
            parts.append("from '{}'".format(self._import_from))

        return " ".join(parts)


class Export(Import):
    keyword = "export"

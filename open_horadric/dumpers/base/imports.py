from __future__ import annotations

import enum
from collections import defaultdict
from typing import DefaultDict
from typing import Dict


class BaseImport:
    class Type(enum.IntEnum):
        UNKNOWN = 0

    def __init__(self, type_: enum.IntEnum, import_name: str, import_from: str = "", import_as: str = ""):
        self._import_name = import_name
        self._import_from = import_from
        self._import_as = import_as
        self.type = type_

    def __str__(self):
        raise NotImplementedError

    def __lt__(self, other: BaseImport):
        if not isinstance(other, self.__class__):
            raise NotImplementedError

        return str(self) < str(other)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise NotImplementedError

        return (
            self.type == other.type
            and self._import_name == other._import_name
            and self._import_as == other._import_as
            and self._import_from == other._import_from
        )


class BaseImports:
    def __init__(self):
        self.parts: DefaultDict[BaseImport.Type, Dict[str, BaseImport]] = defaultdict(dict)

    def add_import(self, import_: BaseImport):
        self.parts[import_.type][str(import_)] = import_

    def __copy__(self):
        copied = self.__class__()
        for imports in self.parts.values():
            for import_str, import_ in imports.items():
                copied.parts[import_.type][import_str] = import_

        return copied

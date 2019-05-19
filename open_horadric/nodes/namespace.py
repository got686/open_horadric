from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Iterable

from open_horadric.nodes.package import Package

if TYPE_CHECKING:
    from open_horadric.nodes.base import BaseNodeType


class Packages(list):
    @property
    def path(self):
        return ".".join(p.name for p in self)


class Namespace(list):
    def __init__(self, iterable: Iterable[BaseNodeType] = ()):
        super().__init__()
        self._packages = Packages()
        self._other = []
        self.extend(iterable)

    @property
    def packages(self) -> Packages:
        return self._packages

    @property
    def other(self):
        return self._other

    def append(self, obj: BaseNodeType):
        if isinstance(obj, Package):
            if self._other:
                raise ValueError("Invalid namespaces order: `Package` after other node types")
            self._packages.append(obj)
        else:
            self._other.append(obj)

        super().append(obj)

    def extend(self, iterable: Iterable[BaseNodeType]):
        for obj in iterable:
            self.append(obj)

    def insert(self, index: int, obj: BaseNodeType):
        if index < 0:
            index = len(self) + index

        if isinstance(obj, Package):
            if self._other and index > len(self._packages):
                raise ValueError("Invalid namespaces order: `Package` after other node types")

            self._packages.insert(index, obj)
        else:
            if index < len(self._packages):
                raise ValueError("Invalid namespaces order: other node after `Package` types")
            self._other.insert(index - len(self._packages), obj)

        super().insert(index, obj)

    def __setitem__(self, index: int, obj: BaseNodeType):
        if index < 0:
            index = len(self) + index

        if isinstance(obj, Package):
            if self._other and index == len(self._packages):
                self._other.pop(0)
                self._packages.append(obj)
            elif self._other and index > len(self._packages):
                raise ValueError("Invalid namespaces order: `Package` after other node types")
            else:
                self._packages[index] = obj
        else:
            if index == len(self._packages) - 1:
                self._packages.pop()
                self._other.insert(0, obj)
            elif index < len(self._packages) - 1:
                raise ValueError("Invalid namespaces order: other node after `Package` types")
            else:
                self._other[index - len(self._packages)] = obj

        super().__setitem__(index, obj)

    def pop(self, index: int = -1):
        if index < 0:
            index = len(self) + index

        if index > len(self._packages):
            self._other.pop(index - len(self._packages))
        else:
            self._packages.pop(index)

        return super().pop(index)

    def clear(self):
        super().clear()
        self._other = []
        self._packages = []

    def remove(self, obj):
        raise NotImplementedError

    def sort(self, *args, **kwargs):
        raise NotImplementedError

    def __iadd__(self, iterable: Iterable[BaseNodeType]):
        self.extend(iterable)
        return self

    def copy(self) -> Namespace:
        # TODO: optimize for not using additional checks
        return Namespace(self)

    def __copy__(self) -> Namespace:
        return self.copy()

    def __deepcopy__(self, memodict={}):
        raise NotImplementedError

    def __add__(self, iterable: Iterable[BaseNodeType]) -> Namespace:
        copied = self.copy()
        copied.extend(iterable)
        return copied

    def __imul__(self, *args, **kwargs):
        raise NotImplementedError

    def insert_package(self, package: Package) -> None:
        self.insert(len(self.packages), package)

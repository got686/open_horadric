from __future__ import annotations

from typing import Type
from typing import TypeVar

from open_horadric.nodes.namespace import Namespace
from open_horadric.nodes.package import Package


class Root(Package):
    def __init__(self):
        super().__init__(name="root", namespace=Namespace(), source_path="", extensions={})

    @property
    def parent(self) -> None:
        return

    def cast_to(self, target_class: Type[RootType]) -> RootType:
        if not issubclass(target_class, Package):
            raise ValueError("`target_class` must be a subclass of `Root`")

        return target_class()


RootType = TypeVar("RootType", bound=Root)

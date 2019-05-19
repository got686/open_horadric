from __future__ import annotations

from typing import Dict
from typing import Type
from typing import TypeVar

from open_horadric.nodes.base import BaseNode
from open_horadric.nodes.base import ExtensionsType
from open_horadric.nodes.namespace import Namespace


class Enum(BaseNode):
    class Value(BaseNode):
        def __init__(self, name: str, namespace: Namespace, source_path: str, extensions: ExtensionsType):
            super().__init__(name, namespace, source_path, extensions)
            self.index: int = None

        def cast_to(self, target_class: Type[EnumValueType]) -> EnumValueType:
            if not issubclass(target_class, Enum.Value):
                raise ValueError("`target_class` must be a subclass of `Enum.Value`")

            return target_class(
                name=self.name, namespace=self.namespace, source_path=self.source_path, extensions=self.extensions
            )

    def __init__(self, name: str, namespace: Namespace, source_path: str, extensions: ExtensionsType):
        super().__init__(name, namespace, source_path, extensions)
        self.values: Dict[str, Enum.Value] = {}

    @property
    def children(self):
        return list(self.values.values())

    def cast_to(self, target_class: Type[EnumType]) -> EnumType:
        if not issubclass(target_class, Enum):
            raise ValueError("`target_class` must be a subclass of `Enum`")

        return target_class(name=self.name, namespace=self.namespace, source_path=self.source_path, extensions=self.extensions)


EnumType = TypeVar("EnumType", bound=Enum)
EnumValueType = TypeVar("EnumValueType", bound=Enum.Value)

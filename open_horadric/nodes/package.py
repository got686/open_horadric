from __future__ import annotations

import itertools
from typing import TYPE_CHECKING
from typing import Dict
from typing import Type
from typing import TypeVar

from open_horadric.nodes.base import BaseNode
from open_horadric.nodes.base import ExtensionsType

if TYPE_CHECKING:
    from open_horadric.nodes.message import Message
    from open_horadric.nodes.enum import Enum
    from open_horadric.nodes.service import Service
    from open_horadric.nodes.namespace import Namespace


class Package(BaseNode):
    def __init__(self, name: str, namespace: Namespace, source_path: str, extensions: ExtensionsType):
        super().__init__(name, namespace, source_path, extensions)
        self.subpackages: Dict[str, Package] = {}
        self.messages: Dict[str, Message] = {}
        self.enums: Dict[str, Enum] = {}
        self.services: Dict[str, Service] = {}

    @property
    def children(self):
        return list(
            itertools.chain(self.subpackages.values(), self.messages.values(), self.enums.values(), self.services.values())
        )

    def cast_to(self, target_class: Type[PackageType]) -> PackageType:
        if not issubclass(target_class, Package):
            raise ValueError("`target_class` must be a subclass of `Package`")

        return target_class(name=self.name, namespace=self.namespace, source_path=self.source_path, extensions=self.extensions)


PackageType = TypeVar("PackageType", bound=Package)

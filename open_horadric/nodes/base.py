from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Dict
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar

from open_horadric.nodes.extension import BaseExtension

if TYPE_CHECKING:
    from open_horadric.nodes.namespace import Namespace

ExtensionsType = Dict[str, BaseExtension]


class BaseNode:
    def __init__(self, name: str, namespace: Namespace[BaseNode], source_path: str, extensions: ExtensionsType):
        self.name = name
        self.namespace = namespace
        self.source_path = source_path
        self.extensions = extensions

    @property
    def parent(self) -> Optional[BaseNode]:
        if len(self.namespace) > 0:
            return self.namespace[-1]

    @property
    def children(self) -> Optional[List[BaseNode]]:
        return []

    def _body_as_str(self, ident_level):
        return "{ident}<{class_name}({name} id='{id}')>".format(
            ident="\t" * ident_level, class_name=self.__class__.__name__, name=self.name, id=id(self)
        )

    def as_str(self, ident_level=0):
        body = self._body_as_str(ident_level=ident_level)

        children = self.children
        if not children:
            return body

        return "{body}:\n{children}".format(
            body=body, children="\n".join(c.as_str(ident_level=ident_level + 1) for c in self.children)
        )

    def __repr__(self) -> str:
        return self.as_str()

    @property
    def full_name(self) -> str:
        return ".".join(node.name for node in self.full_namespace)

    @property
    def full_namespace(self):
        return self.namespace + [self]

    @property
    def full_nested_namespace(self):
        return self.namespace.other

    def cast_to(self, target_class: Type[BaseNodeType]) -> BaseNodeType:
        raise NotImplementedError


BaseNodeType = TypeVar("BaseNodeType", bound=BaseNode)

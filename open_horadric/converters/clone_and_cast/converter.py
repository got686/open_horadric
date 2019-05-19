from __future__ import annotations

from typing import Dict
from typing import Type

from open_horadric.converters.base.converter import BaseConverter
from open_horadric.converters.type_cast.converter import FixSignature
from open_horadric.nodes.base import BaseNode
from open_horadric.nodes.base import BaseNodeType
from open_horadric.nodes.namespace import Namespace
from open_horadric.nodes.root import Root
from open_horadric.nodes.utils import walk_children

__all__ = ("CloneAndCastConverter",)


class CloneAndCastConverter(BaseConverter):
    def __init__(self, clone_and_cast_map: Dict[Type[BaseNode], Type[BaseNode]], fix_map: Dict[Type[BaseNode], FixSignature]):
        self.clone_and_cast_map = clone_and_cast_map
        self.fix_map = fix_map

    def convert(self, root: Root) -> Root:
        source_target_map: Dict[BaseNodeType, BaseNodeType] = {}
        for child in walk_children(root):
            if type(child) in self.clone_and_cast_map:
                source_target_map[child] = self.convert_node(node=child)

        for source, target in source_target_map.items():
            target.namespace = Namespace(source.namespace)
            self.insert_link_to_parent(target=target, source=source)

            fix_func = self.fix_map.get(type(target))
            if fix_func is None:
                raise ValueError("Unknown node type `{}`".format(target.__class__.__name__))
            fix_func(target=target, source=source, source_target_map=source_target_map)

        return source_target_map[root]

    def convert_node(self, node: BaseNodeType):
        return node.cast_to(target_class=self.clone_and_cast_map[node.__class__])

    @staticmethod
    def insert_link_to_parent(target: BaseNode, source: BaseNode):
        raise NotImplementedError

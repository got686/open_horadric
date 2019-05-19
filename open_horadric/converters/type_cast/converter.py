from __future__ import annotations

import copy
from typing import Callable
from typing import Dict
from typing import Type

from open_horadric.converters.base.converter import BaseConverter
from open_horadric.nodes.base import BaseNode
from open_horadric.nodes.base import BaseNodeType
from open_horadric.nodes.enum import Enum
from open_horadric.nodes.message import Message
from open_horadric.nodes.namespace import Namespace
from open_horadric.nodes.package import Package
from open_horadric.nodes.root import Root
from open_horadric.nodes.service import Service
from open_horadric.nodes.utils import walk_children

FixSignature = Callable[[BaseNodeType, BaseNodeType, Dict[BaseNodeType, BaseNodeType]], None]


def fix_package(target: Package, source: Package, source_target_map: Dict[BaseNode, BaseNode]):
    target.subpackages = get_new_nodes(source.subpackages, source_target_map)
    target.messages = get_new_nodes(source.messages, source_target_map)
    target.enums = get_new_nodes(source.enums, source_target_map)
    target.services = get_new_nodes(source.services, source_target_map)
    target.name = source.name


def fix_message(target: Message, source: Message, source_target_map: Dict[BaseNode, BaseNode]):
    target.messages = get_new_nodes(source.messages, source_target_map)
    target.enums = get_new_nodes(source.enums, source_target_map)
    target.fields = get_new_nodes(source.fields, source_target_map)


def fix_field(target: Message.Field, source: Message.Field, source_target_map: Dict[BaseNode, BaseNode]):
    target.index = source.index
    target.container_type = source.container_type
    target.type = source.type
    target.type_name = source.type_name
    target.left_type = source.left_type

    if target.type in (Message.Field.Type.MESSAGE, Message.Field.Type.ENUM):
        target.type_obj = source_target_map[source.type_obj]


def fix_enum(target: Enum, source: Enum, source_target_map: Dict[BaseNode, BaseNode]):
    target.values = get_new_nodes(source.values, source_target_map)


def fix_enum_value(target: Enum.Value, source: Enum.Value, source_target_map: Dict[BaseNode, BaseNode]):
    target.index = source.index


def fix_service(target: Service, source: Service, source_target_map: Dict[BaseNode, BaseNode]):
    target.methods = get_new_nodes(source.methods, source_target_map)


def fix_method(target: Service.Method, source: Service.Method, source_target_map: Dict[BaseNode, BaseNode]):
    target.input_obj = source_target_map[source.input_obj]
    target.output_obj = source_target_map[source.output_obj]
    target.multiple_input = source.multiple_input
    target.multiple_output = source.multiple_output


def get_new_nodes(nodes: Dict[str, BaseNodeType], source_target_map: Dict[BaseNode, BaseNode]) -> Dict[str, BaseNodeType]:
    return {name: source_target_map[node] for name, node in nodes.items()}


class TypeCastConverter(BaseConverter):
    fix_map: Dict[Type[BaseNodeType], FixSignature] = {
        Root: fix_package,
        Package: fix_package,
        Message: fix_message,
        Message.Field: fix_field,
        Enum: fix_enum,
        Enum.Value: fix_enum_value,
        Service: fix_service,
        Service.Method: fix_method,
    }

    def __init__(self, cast_map: Dict[Type[BaseNode], Type[BaseNode]], fix_map_update: dict = None):
        self.cast_map = cast_map
        if fix_map_update:
            self.fix_map = copy.copy(self.fix_map)
            self.fix_map.update(fix_map_update)

    def convert(self, root: Root) -> Root:
        source_target_map: Dict[BaseNodeType, BaseNodeType] = {}
        for child in walk_children(root):
            source_target_map[child] = self.convert_node(node=child)

        # fix for links in new tree
        for child in walk_children(root):
            target = source_target_map[child]
            target.namespace = Namespace([source_target_map[source] for source in child.namespace])
            target.extensions = child.extensions

            fix_func = self.fix_map.get(type(child))
            if fix_func is None:
                raise ValueError("Unknown node type `{}`".format(child.__class__.__name__))
            fix_func(target=target, source=child, source_target_map=source_target_map)

        return source_target_map[root]

    def convert_node(self, node: BaseNodeType):
        if node.__class__ in self.cast_map:
            return node.cast_to(target_class=self.cast_map[node.__class__])
        else:
            # we must create all new structure. No cross trees links
            return node.cast_to(target_class=node.__class__)

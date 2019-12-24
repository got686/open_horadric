from __future__ import annotations

from typing import Dict

from open_horadric.converters.type_cast.converter import fix_message
from open_horadric.converters.type_cast.typescript.interface import FIELDS_TYPES_MAP
from open_horadric.converters.type_cast.typescript.interface import TypescriptMessageInterface
from open_horadric.dumpers.base.jinja2_extensions import in_same_package
from open_horadric.dumpers.base.jinja2_extensions import render_path
from open_horadric.nodes.base import BaseNode
from open_horadric.nodes.base import ExtensionsType
from open_horadric.nodes.enum import Enum
from open_horadric.nodes.namespace import Namespace


class TypescriptMessage(TypescriptMessageInterface):
    class Field(TypescriptMessageInterface.Field):
        @property
        def default_value_string(self) -> str:
            if self.container_type == self.ContainerType.MAP:
                return "{}"
            elif self.container_type == self.ContainerType.LIST:
                return "[]"
            elif self.type == self.type.MESSAGE:
                return "new {}()".format(self._get_message_type_name())
            elif self.type == self.Type.ENUM:
                return "{}.{}".format(self._get_enum_type_name(), list(self.type_obj.values)[0])
            else:
                return {"number": "0", "boolean": "false", "string": "''"}[FIELDS_TYPES_MAP[self.type]]

        @property
        def data_get_value_string(self) -> str:
            not_base_type_template = "data.{} !== undefined ? {{}} : undefined".format(self.name_sting)
            if self.container_type == self.ContainerType.LIST:
                if self.type == self.Type.ENUM:
                    return not_base_type_template.format(
                        "data.{}.map(x => {}[x])".format(self.name_sting, self._get_enum_type_name())
                    )
                elif self.type == self.Type.MESSAGE:
                    return not_base_type_template.format(
                        "data.{}.map({}.FromData)".format(self.name_sting, self._get_message_type_name())
                    )
                else:
                    return "data.{}".format(self.name_sting)
            elif self.container_type == self.ContainerType.MAP:
                if self.type == self.Type.MESSAGE:
                    return self.name_sting
                else:
                    return "data.{}".format(self.name_sting)
            elif self.type == self.Type.ENUM:
                return not_base_type_template.format("{}[data.{}]".format(self._get_enum_type_name(), self.name_sting))
            elif self.type == self.Type.MESSAGE:
                return not_base_type_template.format(
                    "{}.FromData(data.{})".format(self._get_message_type_name(), self.name_sting)
                )
            elif self.type in {self.Type.UINT64, self.Type.FIXED64, self.Type.INT64, self.Type.SFIXED64, self.Type.SINT64}:
                return f"Number(data.{self.name_sting})"

            return f"data.{self.name_sting}"

        def _get_enum_type_name(self):
            if in_same_package(self, self.type_obj):
                return self.type_obj.root_class_name
            else:
                return render_path(self.type_obj.namespace + [self.type_obj.root_class_name])

    def __init__(self, name: str, namespace: Namespace, source_path: str, extensions: ExtensionsType):
        super().__init__(name=name, namespace=namespace, source_path=source_path, extensions=extensions)
        self.interface: TypescriptMessageInterface = None

    @property
    def class_name(self) -> str:
        return self.name

    @property
    def root_class_name(self) -> str:
        return render_path(self.full_namespace.other, delimiter="__")

    def get_from_current_class_name(self, current: TypescriptMessage):
        if in_same_package(self, current):
            return current.root_class_name
        else:
            return "{}.{}".format(render_path(self.namespace.packages), self.root_class_name)


class TypescriptEnum(Enum):
    class Value(Enum.Value):
        pass

    @property
    def class_name(self) -> str:
        return self.name

    @property
    def root_class_name(self) -> str:
        return render_path(self.full_namespace.other, delimiter="__")

    def get_from_current_class_name(self, current: TypescriptMessage):
        if in_same_package(self, current):
            return current.root_class_name
        else:
            return "{}.{}".format(render_path(self.namespace.packages), self.root_class_name)

    @property
    def in_root(self) -> bool:
        return not self.namespace.other


def fix_typescript_message(
    target: TypescriptMessage, source: TypescriptMessageInterface, source_target_map: Dict[BaseNode, BaseNode]
):
    fix_message(target=target, source=source, source_target_map=source_target_map)
    target.interface = source


def copy_typescript_message(target: TypescriptMessage, source: TypescriptMessage, source_target_map: Dict[BaseNode, BaseNode]):
    fix_message(target=target, source=source, source_target_map=source_target_map)
    target.interface = source.interface

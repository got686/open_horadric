from __future__ import annotations

from typing import Optional

from open_horadric.dumpers.base.jinja2_extensions import get_path
from open_horadric.dumpers.base.jinja2_extensions import render_path
from open_horadric.dumpers.base.jinja2_extensions import to_pascal_case
from open_horadric.nodes.message import Message
from open_horadric.nodes.package import Package

TYPES_MAP = {
    Message.Field.Type.DOUBLE: "number",
    Message.Field.Type.FLOAT: "number",
    Message.Field.Type.INT64: "number",
    Message.Field.Type.UINT64: "number",
    Message.Field.Type.INT32: "number",
    Message.Field.Type.FIXED64: "number",
    Message.Field.Type.FIXED32: "number",
    Message.Field.Type.BOOL: "boolean",
    Message.Field.Type.STRING: "string",
    Message.Field.Type.BYTES: "string",  # TODO: find bytes analog
    Message.Field.Type.UINT32: "number",
    Message.Field.Type.SFIXED32: "number",
    Message.Field.Type.SFIXED64: "number",
    Message.Field.Type.SINT32: "number",
    Message.Field.Type.SINT64: "number",
}


class TypescriptMessage(Message):
    class Field(Message.Field):
        def interface_type_name(self, package: Optional[Package] = None):
            # TODO: add type convert map
            if self.container_type == TypescriptMessage.Field.ContainerType.SINGLE:
                if self.type == TypescriptMessage.Field.Type.MESSAGE:
                    return self.type_obj.interface_name(package=package)
                elif self.type == TypescriptMessage.Field.Type.ENUM:
                    return "hz"
                elif self.type in TYPES_MAP:
                    return TYPES_MAP[self.type]
                else:
                    raise ValueError("Unknown field.type {}".format(self.type))
            elif self.container_type == TypescriptMessage.Field.ContainerType.LIST:
                if self.type == TypescriptMessage.Field.Type.MESSAGE:
                    return "{}[]".format(self.type_obj.interface_name(package=package))
                elif self.type == TypescriptMessage.Field.Type.ENUM:
                    return "hz"
                elif self.type in TYPES_MAP:
                    return TYPES_MAP[self.type]
                else:
                    raise ValueError("Unknown field.type {}".format(self.type))
            elif self.container_type == TypescriptMessage.Field.ContainerType.MAP:
                if self.type == TypescriptMessage.Field.Type.MESSAGE:
                    return "{{ [key: {}]: {} }}".format(
                        TYPES_MAP[self.left_type], self.type_obj.interface_name(package=package)
                    )
                elif self.type == TypescriptMessage.Field.Type.ENUM:
                    return "hz"
                elif self.type in TYPES_MAP:
                    return TYPES_MAP[self.type]
                else:
                    raise ValueError("Unknown field.type {}".format(self.type))
            else:
                raise ValueError("Unknown field.container_type {}".format(self.container_type))

        def data_interface_type_name(self, package: Optional[Package] = None):
            return "hz"

    def interface_name(self, package: Package = None):
        pascal_case_name = to_pascal_case(self.name)
        if package is None:
            return "I{}".format(pascal_case_name)
        else:
            full_path = get_path(node=self, namespace=package.namespace, file_name="interfaces")
            return render_path(full_path[:-1] + ["I{}".format(pascal_case_name)])

    def data_interface_name(self, package: Package = None):
        return "{}Data".format(self.interface_name(package=package))

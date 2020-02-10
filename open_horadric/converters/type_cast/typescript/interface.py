from __future__ import annotations

from open_horadric.dumpers.base.jinja2_extensions import in_same_package
from open_horadric.dumpers.base.jinja2_extensions import render_path
from open_horadric.dumpers.base.jinja2_extensions import to_camel_case
from open_horadric.nodes.message import Message

FIELDS_TYPES_MAP = {
    Message.Field.Type.DOUBLE: "number",
    Message.Field.Type.FLOAT: "number",
    Message.Field.Type.INT64: "number",
    Message.Field.Type.UINT64: "number",
    Message.Field.Type.INT32: "number",
    Message.Field.Type.FIXED64: "number",
    Message.Field.Type.FIXED32: "number",
    Message.Field.Type.BOOL: "boolean",
    Message.Field.Type.STRING: "string",
    Message.Field.Type.BYTES: "string",  # TODO: find specific typescript bytes field
    Message.Field.Type.UINT32: "number",
    Message.Field.Type.SFIXED32: "number",
    Message.Field.Type.SFIXED64: "number",
    Message.Field.Type.SINT32: "number",
    Message.Field.Type.SINT64: "number",
}


class TypescriptMessageInterface(Message):
    class Field(Message.Field):
        @property
        def type_name_string(self) -> str:
            if self.type == self.Type.MESSAGE:
                type_string = self._get_message_type_name()
            elif self.type == self.Type.ENUM:
                type_string = "keyof typeof {}".format(self._get_enum_type_name())
            else:
                type_string = FIELDS_TYPES_MAP[self.type]

            if self.container_type == self.ContainerType.LIST:
                return "{}[]".format(type_string)
            elif self.container_type == self.ContainerType.MAP:
                return "{{ [key: {}]: {} }}".format(FIELDS_TYPES_MAP[self.left_type], type_string)
            else:
                return type_string

        @property
        def data_type_name_string(self) -> str:
            if self.type in {self.Type.SINT64, self.Type.SFIXED64, self.Type.INT64, self.Type.FIXED64, self.Type.UINT64}:
                return "string"

            return self.type_name_string

        @property
        def name_sting(self) -> str:
            return to_camel_case(self.name)

        def _get_message_type_name(self) -> str:
            if in_same_package(self, self.type_obj):
                return self.type_obj.root_class_name
            else:
                return render_path(self.type_obj.namespace + [self.type_obj.root_class_name])

        def _get_enum_type_name(self) -> str:
            return render_path(self.type_obj.full_namespace)

    @property
    def class_name(self) -> str:
        return "I{}".format(self.name)

    @property
    def data_class_name(self) -> str:
        return "I{}Data".format(self.name)

    @property
    def root_class_name(self) -> str:
        return render_path(self.namespace.other + [self.class_name], delimiter="__")

    @property
    def data_root_class_name(self) -> str:
        if self.namespace.other:
            return "{}__{}".format(render_path(self.namespace.other, delimiter="__"), self.data_class_name)
        else:
            return self.data_class_name

    @property
    def in_root(self) -> bool:
        return not self.namespace.other

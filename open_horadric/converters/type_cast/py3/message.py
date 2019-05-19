from __future__ import annotations

from google.protobuf.internal.well_known_types import WKTBASES

from open_horadric.dumpers.base.jinja2_extensions import in_same_package
from open_horadric.dumpers.base.jinja2_extensions import render_path
from open_horadric.nodes.message import Message

FIELDS_TYPES_MAP = {
    Message.Field.Type.DOUBLE: "float",
    Message.Field.Type.FLOAT: "float",
    Message.Field.Type.INT64: "int",
    Message.Field.Type.UINT64: "int",
    Message.Field.Type.INT32: "int",
    Message.Field.Type.FIXED64: "int",
    Message.Field.Type.FIXED32: "int",
    Message.Field.Type.BOOL: "bool",
    Message.Field.Type.STRING: "str",
    Message.Field.Type.BYTES: "bytes",
    Message.Field.Type.UINT32: "int",
    Message.Field.Type.SFIXED32: "int",
    Message.Field.Type.SFIXED64: "int",
    Message.Field.Type.SINT32: "int",
    Message.Field.Type.SINT64: "int",
}


class Py3Message(Message):
    class Field(Message.Field):
        @property
        def _source_type_string(self) -> str:
            if self.type in (self.Type.MESSAGE, self.type.ENUM):
                if in_same_package(self, self.type_obj):
                    return self.type_obj.name
                else:
                    return render_path(self.type_obj.full_namespace)
            else:
                return FIELDS_TYPES_MAP[self.type]

        @property
        def type_string(self) -> str:
            type_string = self._source_type_string

            if self.container_type == self.ContainerType.LIST:
                if self.type in (self.Type.MESSAGE, self.type.ENUM):
                    return "RepeatedCompositeFieldContainer[{}]".format(type_string)
                else:
                    return "RepeatedScalarFieldContainer[{}]".format(type_string)
            elif self.container_type == self.ContainerType.MAP:
                if self.type in (self.Type.MESSAGE, self.type.ENUM):
                    return "MessageMap[{}, {}]".format(FIELDS_TYPES_MAP[self.left_type], type_string)
                else:
                    return "ScalarMap[{}, {}]".format(FIELDS_TYPES_MAP[self.left_type], type_string)
            else:
                return type_string

        @property
        def init_type_string(self) -> str:
            type_string = self._source_type_string

            if self.container_type == self.ContainerType.LIST:
                return "List[{}]".format(type_string)
            elif self.container_type == self.ContainerType.MAP:
                return "Dict[{}, {}]".format(FIELDS_TYPES_MAP[self.left_type], type_string)
            else:
                return type_string

        @property
        def default_value_string(self) -> str:
            if self.container_type in (self.ContainerType.MAP, self.ContainerType.LIST):
                return "None"
            elif self.type in (self.Type.MESSAGE, self.Type.ENUM):
                return "None"
            else:
                return {"int": "0", "float": "0", "bool": "False", "str": "''", "bytes": "b''"}[FIELDS_TYPES_MAP[self.type]]

    @property
    def no_package_type_string(self) -> str:
        return render_path(self.full_namespace.other)

    @property
    def parents_sting(self) -> str:
        if self.in_well_known_types:
            return "Message, Protobuf{}".format(self.name)
        else:
            return "Message"

    @property
    def in_well_known_types(self) -> bool:
        return ".".join([p.name for p in self.namespace.packages[1:-1]] + [self.name]) in WKTBASES

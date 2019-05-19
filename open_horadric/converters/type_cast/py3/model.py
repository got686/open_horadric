from __future__ import annotations

from typing import Dict
from typing import List
from typing import Union

from open_horadric.converters.type_cast.converter import fix_field
from open_horadric.converters.type_cast.converter import fix_message
from open_horadric.dumpers.base.jinja2_extensions import in_same_package
from open_horadric.dumpers.base.jinja2_extensions import render_path
from open_horadric.dumpers.py3.imports import Import
from open_horadric.nodes.base import BaseNode
from open_horadric.nodes.base import ExtensionsType
from open_horadric.nodes.enum import Enum
from open_horadric.nodes.message import Message
from open_horadric.nodes.namespace import Namespace

FIELDS_TYPES_MAP = {
    Message.Field.Type.DOUBLE: "Float",
    Message.Field.Type.FLOAT: "Float",
    Message.Field.Type.INT64: "BigInteger",
    Message.Field.Type.UINT64: "BigInteger",
    Message.Field.Type.INT32: "Integer",
    Message.Field.Type.FIXED64: "BigInteger",
    Message.Field.Type.FIXED32: "BigInteger",
    Message.Field.Type.BOOL: "Boolean",
    Message.Field.Type.STRING: "Text",
    Message.Field.Type.BYTES: "LargeBinary",
    Message.Field.Type.UINT32: "Integer",
    Message.Field.Type.SFIXED32: "Integer",
    Message.Field.Type.SFIXED64: "BigInteger",
    Message.Field.Type.SINT32: "Integer",
    Message.Field.Type.SINT64: "BigInteger",
}


class Py3Model(Message):
    def __init__(self, name: str, namespace: Namespace, source_path: str, extensions: ExtensionsType):
        super().__init__(name, namespace, source_path, extensions)
        self.message: Message = None

    class Field(Message.Field):
        def __init__(self, name: str, namespace: Namespace, source_path: str, extensions: ExtensionsType):
            super().__init__(name, namespace, source_path, extensions)
            self.message_field: Message.Field = None

        @property
        def is_primary_key(self):
            return self.extensions["db.primary_key"].value

        @property
        def type_string(self) -> str:
            column_type = self.column_type
            if isinstance(column_type, str):
                return "{}()".format(column_type)
            elif isinstance(column_type, Enum):
                if in_same_package(self, column_type):
                    return "Enum({})".format(render_path(column_type.full_namespace.other))
                else:
                    return "Enum({})".format(render_path(column_type.full_namespace))
            elif isinstance(column_type, Py3Model):
                return ""  # TODO: fixme
            else:
                raise ValueError("Unknown field `column_type`: {}".format(column_type))

        @property
        def blob_string(self) -> str:
            return "JSON"

        @property
        def define_strings(self) -> List[str]:
            kwargs = {}
            column_type = self.column_type
            if isinstance(column_type, (str, Enum)):
                type_string = self.type_string
            else:
                if column_type.is_model:
                    pks = [f for f in column_type.fields.values() if f.is_primary_key]
                    return ["{}_{} = Column({})".format(self.name, pk.name, pk.type_string) for pk in pks]
                else:
                    type_string = "{}()".format(self.blob_string)

            if kwargs:
                return [
                    "{} = Column({}, {})".format(
                        self.name, type_string, ", ".join("{}={}".format(k, v) for k, v in kwargs.items())
                    )
                ]
            else:
                return ["{} = Column({})".format(self.name, type_string)]

        @property
        def column_type(self) -> Union[str, Py3Model]:
            if self.container_type in (self.ContainerType.LIST, self.ContainerType.MAP):  # ARRAY in postgresql
                return "JSON"
            elif self.type in (self.Type.MESSAGE, self.type.ENUM):
                return self.type_obj
            else:
                return FIELDS_TYPES_MAP[self.type]

        @property
        def type_imports(self) -> List[Import]:
            column_type = self.column_type
            if isinstance(column_type, str):
                return [Import(type_=Import.Type.LIBRARY, import_name=column_type, import_from="sqlalchemy")]
            elif isinstance(column_type, Enum):
                if in_same_package(self, column_type):
                    return [
                        Import(
                            type_=Import.Type.LOCAL,
                            import_name=self.message_field.type_obj.namespace.other[0].name,
                            import_from=render_path(self.message_field.namespace.packages),
                        ),
                        Import(type_=Import.Type.LIBRARY, import_name="Enum", import_from="sqlalchemy"),
                    ]
                else:
                    return [
                        Import(
                            type_=Import.Type.LOCAL, import_name=render_path(self.message_field.type_obj.namespace.packages)
                        ),
                        Import(type_=Import.Type.LIBRARY, import_name="Enum", import_from="sqlalchemy"),
                    ]
            elif isinstance(column_type, Message):
                if not self.is_relationship:
                    return []

                imports = [Import(type_=Import.Type.LIBRARY, import_name="relationship", import_from="sqlalchemy.orm")]
                if in_same_package(self, column_type):
                    return imports
                else:
                    imports.append(Import(type_=Import.Type.LOCAL, import_name=render_path(column_type.namespace.packages)))
                    return imports
            else:
                return [Import(type_=Import.Type.LOCAL, import_name=render_path(column_type.namespace.packages))]

        @property
        def is_relationship(self) -> bool:
            if not self.type == self.Type.MESSAGE:
                return False

            if not self.type_obj.is_model:
                return False

            return True

    @property
    def is_model(self):
        return self.extensions["db.table"].value

    @property
    def class_name(self) -> str:
        return "{}Model".format(self.name)

    @property
    def relationships_strings(self) -> List[str]:
        relationships = []
        for field in self.fields.values():  # type: Py3Model.Field
            column_type = field.column_type
            if isinstance(column_type, Py3Model) and column_type.is_model:
                if in_same_package(self, column_type):
                    relationships.append(
                        "{} = relationship('{}')".format(
                            field.name, render_path(column_type.namespace.other + [column_type.class_name])
                        )
                    )
                else:
                    relationships.append(
                        "{} = relationship('{}')".format(
                            field.name, render_path(column_type.namespace + [column_type.class_name])
                        )
                    )
            # else:
            #     raise ValueError("Relationship must be only with other model")

        return relationships

    @property
    def constraints_strings(self) -> List[str]:
        return []

    @property
    def fields_strings(self) -> List[str]:
        result = []
        for field in self.fields.values():  # type: Py3Model.Field
            result.extend(field.define_strings)

        return result


def fix_model(target: Py3Model, source: Message, source_target_map: Dict[BaseNode, BaseNode]):
    fix_message(target=target, source=source, source_target_map=source_target_map)
    target.message = source


def fix_model_field(target: Py3Model.Field, source: Message.Field, source_target_map: Dict[BaseNode, BaseNode]):
    fix_field(target=target, source=source, source_target_map=source_target_map)
    target.message_field = source

from __future__ import annotations

import enum
import itertools
from typing import TYPE_CHECKING
from typing import Dict
from typing import Type
from typing import TypeVar
from typing import Union

from open_horadric.nodes.base import BaseNode
from open_horadric.nodes.base import ExtensionsType

if TYPE_CHECKING:
    from open_horadric.nodes.enum import Enum
    from open_horadric.nodes.namespace import Namespace


class Message(BaseNode):
    class Field(BaseNode):
        class Type(enum.IntEnum):
            # Values must have indexes same as in google.protobuf.descriptor.FieldDescriptor.TYPE_*
            DOUBLE = 1
            FLOAT = 2
            INT64 = 3
            UINT64 = 4
            INT32 = 5
            FIXED64 = 6
            FIXED32 = 7
            BOOL = 8
            STRING = 9
            # GROUP = 10
            MESSAGE = 11
            BYTES = 12
            UINT32 = 13
            ENUM = 14
            SFIXED32 = 15
            SFIXED64 = 16
            SINT32 = 17
            SINT64 = 18

        class ContainerType(enum.IntEnum):
            SINGLE = 0
            LIST = 1
            MAP = 2

        def __init__(self, name: str, namespace: Namespace, source_path: str, extensions: ExtensionsType):
            super().__init__(name, namespace, source_path, extensions)
            self.index: int = None
            self.container_type: Message.Field.ContainerType = Message.Field.ContainerType.SINGLE
            self.type: Message.Field.Type = None
            self.type_name: str = None
            self.type_obj: Union[Message, Enum] = None
            self.left_type: Message.Field.Type = None  # set only on DICT container type

        def _body_as_str(self, ident_level):
            template = "{ident}<{class_name}({name} ({type_value}) id='{id}')>"

            if self.container_type == self.ContainerType.MAP:
                if self.type in (self.Type.ENUM, self.Type.MESSAGE):
                    type_name = self.type_name
                else:
                    type_name = self.type.name

                type_value = "<map({},{})>".format(self.left_type.name, type_name)
            elif self.container_type == self.ContainerType.LIST:
                if self.type in (self.Type.ENUM, self.Type.MESSAGE):
                    type_name = self.type_name
                else:
                    type_name = self.type.name

                type_value = "<list({})>".format(type_name)
            else:
                if self.type in (self.Type.ENUM, self.Type.MESSAGE):
                    type_value = self.type_name
                else:
                    type_value = self.type.name

            return template.format(
                ident="\t" * ident_level, class_name=self.__class__.__name__, name=self.name, type_value=type_value, id=id(self)
            )

        def cast_to(self, target_class: Type[MessageFieldType]) -> MessageFieldType:
            if not issubclass(target_class, Message.Field):
                raise ValueError("`target_class` must be a subclass of `Message.Field`")

            return target_class(
                name=self.name, namespace=self.namespace, source_path=self.source_path, extensions=self.extensions
            )

    def __init__(self, name: str, namespace: Namespace, source_path: str, extensions: ExtensionsType):
        super().__init__(name, namespace, source_path, extensions)
        self.messages: Dict[str, Message] = {}
        self.enums: Dict[str, Enum] = {}
        self.fields: Dict[str, Message.Field] = {}

    @property
    def children(self):
        return list(itertools.chain(self.messages.values(), self.enums.values(), self.fields.values()))

    def cast_to(self, target_class: Type[MessageType]) -> MessageType:
        if not issubclass(target_class, Message):
            raise ValueError("`target_class` must be a subclass of `Message`")

        return target_class(name=self.name, namespace=self.namespace, source_path=self.source_path, extensions=self.extensions)


MessageType = TypeVar("MessageType", bound=Message)
MessageFieldType = TypeVar("MessageFieldType", bound=Message.Field)

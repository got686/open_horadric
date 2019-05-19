from __future__ import annotations

import logging
from typing import List
from typing import Union

from google.protobuf.descriptor import FieldDescriptor
from google.protobuf.descriptor_pb2 import DescriptorProto
from google.protobuf.descriptor_pb2 import EnumDescriptorProto
from google.protobuf.descriptor_pb2 import FieldDescriptorProto
from google.protobuf.descriptor_pb2 import FileDescriptorProto
from google.protobuf.descriptor_pb2 import ServiceDescriptorProto

from open_horadric.nodes.base import ExtensionsType
from open_horadric.nodes.enum import Enum
from open_horadric.nodes.extension import BaseExtension
from open_horadric.nodes.message import Message
from open_horadric.nodes.package import Package
from open_horadric.nodes.root import Root
from open_horadric.nodes.service import Service
from open_horadric.parsers.base.parser import BaseParser
from open_horadric.parsers.proto3.indexer import Proto3Indexer
from open_horadric.parsers.proto3.indexer import Proto3Indexes
from open_horadric.parsers.proto3.source import FileSource
from open_horadric.parsers.proto3.types_resolver import TypesResolver

logger = logging.getLogger("open_horadric.parsers.proto3")


class Proto3Parser(BaseParser):
    def parse(self, sources: List[FileSource]) -> Root:
        # logger.info('Start parsing with: %s', sources)
        proto_indexes = Proto3Indexer().index(s.content for s in sources)

        root = Root()
        for source in sources:
            package = self._add_packages(root=root, path=source.content.package, source_path=source.path)
            self._add_messages(
                current_node=package, source=source.content, proto_indexes=proto_indexes, source_path=source.path
            )
            self._add_enums(current_node=package, source=source.content, source_path=source.path)
            self._add_services(current_node=package, source=source.content, source_path=source.path)

        TypesResolver().resolve(root=root)
        logger.info("Parse result:\n%s", root.as_str(ident_level=1))
        return root

    @classmethod
    def _add_packages(cls, root: Root, path: str, source_path: str) -> Package:
        current_node = root
        parts = path.split(".")

        for i, part in enumerate(parts):
            next_node = current_node.subpackages.get(part)

            if next_node is None:
                next_node = Package(
                    name=part, namespace=current_node.namespace + [current_node], source_path=source_path, extensions={}
                )
                current_node.subpackages[part] = next_node

            current_node = next_node

        return current_node

    def _add_messages(
        self,
        current_node: Union[Package, Message],
        source: Union[FileDescriptorProto, DescriptorProto],
        proto_indexes: Proto3Indexes,
        source_path: str,
    ):
        if isinstance(source, FileDescriptorProto):
            messages_sources = source.message_type
        else:
            messages_sources = source.nested_type

        for message_proto in messages_sources:
            # ignore map entry, it is field options
            if message_proto.options.map_entry:
                continue

            message = Message(
                name=message_proto.name,
                namespace=current_node.namespace + [current_node],
                source_path=source_path,
                extensions=self._get_extensions(message_proto),
            )

            current_node.messages[message_proto.name] = message
            self._add_messages(current_node=message, source=message_proto, proto_indexes=proto_indexes, source_path=source_path)
            self._add_enums(current_node=message, source=message_proto, source_path=source_path)
            self._add_message_fields(
                current_node=message, source=message_proto, proto_indexes=proto_indexes, source_path=source_path
            )

    def _add_message_fields(
        self, current_node: Message, source: DescriptorProto, proto_indexes: Proto3Indexes, source_path: str
    ):
        for field_proto in source.field:
            message_field = Message.Field(
                name=field_proto.name,
                namespace=current_node.namespace + [current_node],
                source_path=source_path,
                extensions=self._get_extensions(field_proto),
            )
            if field_proto.type == FieldDescriptor.TYPE_MESSAGE:
                message_proto = proto_indexes[DescriptorProto][field_proto.type_name]
                if message_proto.options.map_entry:
                    message_field.container_type = message_field.ContainerType.MAP

                    left = message_proto.field[0]
                    right = message_proto.field[1]

                    message_field.left_type = Message.Field.Type._value2member_map_[left.type]
                    message_field.type = Message.Field.Type._value2member_map_[right.type]

                    if right.type in (FieldDescriptor.TYPE_ENUM, FieldDescriptor.TYPE_MESSAGE):
                        message_field.type_name = self._get_field_type_path(right)

                else:
                    message_field.type = Message.Field.Type.MESSAGE
                    message_field.type_name = self._get_field_type_path(field_proto)
                    if field_proto.label == FieldDescriptor.LABEL_REPEATED:
                        message_field.container_type = message_field.ContainerType.LIST

            elif field_proto.type == FieldDescriptor.TYPE_ENUM:
                message_field.type = Message.Field.Type.ENUM
                message_field.type_name = self._get_field_type_path(field_proto)
                if field_proto.label == FieldDescriptor.LABEL_REPEATED:
                    message_field.container_type = message_field.ContainerType.LIST

            else:
                message_field.type = Message.Field.Type._value2member_map_[field_proto.type]
                if field_proto.label == FieldDescriptor.LABEL_REPEATED:
                    message_field.container_type = message_field.ContainerType.LIST

            # type type_name label
            message_field.index = field_proto.number
            current_node.fields[field_proto.name] = message_field

    def _add_enums(
        self, current_node: Union[Package, Message], source: Union[FileDescriptorProto, DescriptorProto], source_path: str
    ):
        for enum_proto in source.enum_type:
            enum = Enum(
                name=enum_proto.name,
                namespace=current_node.namespace + [current_node],
                source_path=source_path,
                extensions=self._get_extensions(enum_proto),
            )

            current_node.enums[enum_proto.name] = enum
            self._add_enum_values(current_node=enum, source=enum_proto, source_path=source_path)

    def _add_enum_values(self, current_node: Enum, source: EnumDescriptorProto, source_path: str):
        for enum_value_proto in source.value:
            enum_value = Enum.Value(
                name=enum_value_proto.name,
                namespace=current_node.namespace + [current_node],
                source_path=source_path,
                extensions=self._get_extensions(enum_value_proto),
            )
            enum_value.index = enum_value_proto.number
            current_node.values[enum_value_proto.name] = enum_value

    def _add_services(self, current_node: Package, source: FileDescriptorProto, source_path: str):
        for service_proto in source.service:
            service = Service(
                name=service_proto.name,
                namespace=current_node.namespace + [current_node],
                source_path=source_path,
                extensions=self._get_extensions(service_proto),
            )

            current_node.services[service_proto.name] = service
            self._add_service_methods(current_node=service, source=service_proto, source_path=source_path)

    def _add_service_methods(self, current_node: Service, source: ServiceDescriptorProto, source_path: str):
        for method_proto in source.method:
            method = Service.Method(
                name=method_proto.name,
                namespace=current_node.namespace + [current_node],
                source_path=source_path,
                extensions=self._get_extensions(method_proto),
            )
            method.input_name = method_proto.input_type[1:]  # do not include start '.'
            method.output_name = method_proto.output_type[1:]  # do not include start '.'
            method.multiple_input = method_proto.client_streaming
            method.multiple_output = method_proto.server_streaming

            current_node.methods[method_proto.name] = method

    @staticmethod
    def _get_field_type_path(descriptor: FieldDescriptorProto):
        return descriptor.type_name[1:]  # do not include start '.'

    @staticmethod
    def _get_extensions(descriptor: DescriptorProto) -> ExtensionsType:
        exts = {
            n: BaseExtension(name=n, value=descriptor.options.Extensions[ext])
            for n, ext in descriptor.options._extensions_by_name.items()
        }

        return exts

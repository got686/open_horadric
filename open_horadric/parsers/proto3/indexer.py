from __future__ import annotations

import logging
from itertools import chain
from typing import DefaultDict
from typing import Dict
from typing import List
from typing import Type
from typing import Union

from google.protobuf.descriptor_pb2 import DescriptorProto
from google.protobuf.descriptor_pb2 import EnumDescriptorProto
from google.protobuf.descriptor_pb2 import EnumValueDescriptorProto
from google.protobuf.descriptor_pb2 import FieldDescriptorProto
from google.protobuf.descriptor_pb2 import FileDescriptorProto
from google.protobuf.descriptor_pb2 import MethodDescriptorProto
from google.protobuf.descriptor_pb2 import ServiceDescriptorProto

from open_horadric.base.indexer import BaseTreeIndexer

Descriptor = Union[
    FileDescriptorProto,
    DescriptorProto,
    FieldDescriptorProto,
    EnumDescriptorProto,
    EnumValueDescriptorProto,
    ServiceDescriptorProto,
    MethodDescriptorProto,
]

DescriptorType = Type[Descriptor]
Path = List[Descriptor]

Proto3Indexes = DefaultDict[Union[str, DescriptorType], Dict[str, Descriptor]]

ALL = "__all__"

logger = logging.getLogger("open_horadric.parsers.proto3")


class Proto3Indexer(BaseTreeIndexer):
    get_children_map = {
        FileDescriptorProto: lambda d: tuple(chain(d.message_type, d.enum_type, d.service)),
        DescriptorProto: lambda d: tuple(chain(d.nested_type, d.enum_type)),
        FieldDescriptorProto: lambda d: (),
        EnumDescriptorProto: lambda d: tuple(d.value),
        EnumValueDescriptorProto: lambda d: (),
        ServiceDescriptorProto: lambda d: tuple(d.method),
        MethodDescriptorProto: lambda d: (),
    }

    def get_path_str(self, obj: Descriptor, path: List[Descriptor]):
        if isinstance(obj, FileDescriptorProto):
            return obj.name
        else:
            return ".{}.{}".format(path[0].package, ".".join(d.name for d in path[1:]))

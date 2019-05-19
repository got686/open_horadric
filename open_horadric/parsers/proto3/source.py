from __future__ import annotations

from dataclasses import dataclass

from google.protobuf.descriptor_pb2 import FileDescriptorProto

from open_horadric.parsers.base.source import BaseSource


@dataclass
class FileSource(BaseSource):
    content: FileDescriptorProto

    @classmethod
    def from_descriptor(cls, descriptor: FileDescriptorProto) -> FileSource:
        return cls(path=descriptor.name, content=descriptor, source_content="")

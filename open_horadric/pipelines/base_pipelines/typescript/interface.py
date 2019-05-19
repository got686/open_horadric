from __future__ import annotations

from open_horadric.converters.files_converter.converter import FilesConverter
from open_horadric.converters.type_cast.converter import TypeCastConverter
from open_horadric.converters.type_cast.typescript.interface import TypescriptMessageInterface
from open_horadric.dumpers.typescript.interfaces_dumper import TypescriptInterfacesDumper
from open_horadric.nodes.enum import Enum
from open_horadric.nodes.message import Message
from open_horadric.pipelines.pipeline import PipelineTreeNode

typescript_interfaces_subtree = PipelineTreeNode(
    converter=TypeCastConverter(cast_map={Message: TypescriptMessageInterface, Message.Field: TypescriptMessageInterface.Field})
)

typescript_interfaces_subtree.children.append(
    PipelineTreeNode(
        converter=FilesConverter(
            type_file_map={
                TypescriptMessageInterface: "interfaces",
                TypescriptMessageInterface.Field: "interfaces",
                Enum: "messages",
                Enum.Value: "messages",
            }
        ),
        dumpers=[TypescriptInterfacesDumper()],
    )
)

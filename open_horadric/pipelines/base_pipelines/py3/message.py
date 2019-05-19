from __future__ import annotations

from open_horadric.converters.files_converter.converter import FilesConverter
from open_horadric.converters.type_cast.converter import TypeCastConverter
from open_horadric.converters.type_cast.py3.message import Py3Message
from open_horadric.dumpers.py3.message_dumper import Py3MessageDumper
from open_horadric.nodes.enum import Enum
from open_horadric.nodes.message import Message
from open_horadric.pipelines.pipeline import PipelineTreeNode

py3_messages_subtree = PipelineTreeNode(
    converter=FilesConverter(
        type_file_map={Message: "messages", Message.Field: "messages", Enum: "messages", Enum.Value: "messages"}
    )
)

py3_messages_subtree.children.append(
    PipelineTreeNode(
        converter=TypeCastConverter(
            cast_map={Message: Py3Message, Message.Field: Py3Message.Field, Enum: Enum, Enum.Value: Enum.Value}
        ),
        dumpers=[Py3MessageDumper()],
    )
)

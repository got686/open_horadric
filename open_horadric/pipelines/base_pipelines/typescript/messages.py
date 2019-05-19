from __future__ import annotations

from open_horadric.converters.package_rename_converter.converter import PackageRenameConverter
from open_horadric.converters.type_cast.converter import TypeCastConverter
from open_horadric.converters.type_cast.converter import fix_field
from open_horadric.converters.type_cast.typescript.interface import TypescriptMessageInterface
from open_horadric.converters.type_cast.typescript.message import TypescriptEnum
from open_horadric.converters.type_cast.typescript.message import TypescriptMessage
from open_horadric.converters.type_cast.typescript.message import fix_typescript_message
from open_horadric.dumpers.typescript.messages_dumper import TypescriptMessagesDumper
from open_horadric.nodes.enum import Enum
from open_horadric.pipelines.pipeline import PipelineTreeNode

typescript_messages_subtree = PipelineTreeNode(
    converter=TypeCastConverter(
        cast_map={
            TypescriptMessageInterface: TypescriptMessage,
            TypescriptMessageInterface.Field: TypescriptMessage.Field,
            Enum: TypescriptEnum,
            Enum.Value: TypescriptEnum.Value,
        },
        fix_map_update={TypescriptMessageInterface: fix_typescript_message, TypescriptMessageInterface.Field: fix_field},
    )
)

typescript_messages_subtree.children.append(
    PipelineTreeNode(
        converter=PackageRenameConverter(rule=lambda package: "messages" if package.name == "interfaces" else None),
        dumpers=[TypescriptMessagesDumper()],
    )
)

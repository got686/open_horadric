from __future__ import annotations

from open_horadric.converters.files_converter.converter import FilesConverter
from open_horadric.converters.type_cast.converter import TypeCastConverter
from open_horadric.converters.type_cast.converter import fix_enum
from open_horadric.converters.type_cast.converter import fix_enum_value
from open_horadric.converters.type_cast.converter import fix_field
from open_horadric.converters.type_cast.typescript.client import TypescriptClient
from open_horadric.converters.type_cast.typescript.message import TypescriptEnum
from open_horadric.converters.type_cast.typescript.message import TypescriptMessage
from open_horadric.converters.type_cast.typescript.message import copy_typescript_message
from open_horadric.dumpers.typescript.clients_dumper import TypescriptClientsDumper
from open_horadric.nodes.service import Service
from open_horadric.pipelines.pipeline import PipelineTreeNode

typescript_clients_subtree = PipelineTreeNode(
    converter=TypeCastConverter(
        cast_map={Service: TypescriptClient, Service.Method: TypescriptClient.Method},
        fix_map_update={
            TypescriptMessage: copy_typescript_message,
            TypescriptMessage.Field: fix_field,
            TypescriptEnum: fix_enum,
            TypescriptEnum.Value: fix_enum_value,
        },
    )
)

typescript_clients_subtree.children.append(
    PipelineTreeNode(
        converter=FilesConverter(type_file_map={TypescriptClient: "clients", TypescriptClient.Method: "clients"}),
        dumpers=[TypescriptClientsDumper()],
    )
)

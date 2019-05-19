from __future__ import annotations

from open_horadric.converters.files_converter.converter import FilesConverter
from open_horadric.converters.type_cast.converter import TypeCastConverter
from open_horadric.converters.type_cast.converter import fix_field
from open_horadric.converters.type_cast.converter import fix_message
from open_horadric.converters.type_cast.py3.message import Py3Message
from open_horadric.converters.type_cast.py3.server import Py3Server
from open_horadric.dumpers.py3.server_dumper import Py3ServerDumper
from open_horadric.nodes.service import Service
from open_horadric.pipelines.pipeline import PipelineTreeNode

py3_server_subtree = PipelineTreeNode(
    converter=TypeCastConverter(
        cast_map={Service: Py3Server, Service.Method: Py3Server.Method},
        fix_map_update={Py3Message: fix_message, Py3Message.Field: fix_field},
    )
)

py3_server_subtree.children.append(
    PipelineTreeNode(
        converter=FilesConverter(type_file_map={Py3Server: "server", Py3Server.Method: "server"}), dumpers=[Py3ServerDumper()]
    )
)

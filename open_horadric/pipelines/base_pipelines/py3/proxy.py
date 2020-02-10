from __future__ import annotations

from open_horadric.config.config import Config
from open_horadric.converters.package_rename_converter.converter import PackageRenameConverter
from open_horadric.converters.root_folder.converter import RootFolderConverter
from open_horadric.converters.type_cast.converter import TypeCastConverter
from open_horadric.converters.type_cast.converter import fix_field
from open_horadric.converters.type_cast.converter import fix_message
from open_horadric.converters.type_cast.py3.client import Py3Client
from open_horadric.converters.type_cast.py3.message import Py3Message
from open_horadric.converters.type_cast.py3.proxy import Py3Proxy
from open_horadric.converters.type_cast.py3.proxy import fix_proxy_method
from open_horadric.converters.type_cast.py3.proxy import fix_proxy_service
from open_horadric.dumpers.proxy.dumper import ProxyDumper
from open_horadric.pipelines.pipeline import PipelineTreeNode

config = Config()

# must be first because it clones packages tree
py3_proxy_subtree = PipelineTreeNode(
    converter=TypeCastConverter(
        cast_map={Py3Client: Py3Proxy, Py3Client.Method: Py3Proxy.Method},
        fix_map_update={
            Py3Message: fix_message,
            Py3Message.Field: fix_field,
            Py3Client: fix_proxy_service,
            Py3Client.Method: fix_proxy_method,
        },
    )
)

py3_proxy_subtree.children.append(
    PipelineTreeNode(
        converter=RootFolderConverter(folder_name="{}_{}".format(config.project_name, config.pipelines["proxy"]["root_suffix"]))
    )
)

py3_proxy_subtree.children[0].children.append(
    PipelineTreeNode(
        converter=PackageRenameConverter(rule=lambda package: "proxy" if package.name == "client" else None),
        dumpers=[ProxyDumper(cors=config.pipelines["proxy"]["dumpers"]["proxy"]["cors"])],
    )
)

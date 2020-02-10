from __future__ import annotations

from open_horadric.config.config import Config
from open_horadric.converters.root_folder.converter import RootFolderConverter
from open_horadric.pipelines.base_pipelines.py3.client import py3_client_subtree
from open_horadric.pipelines.base_pipelines.py3.message import py3_messages_subtree
from open_horadric.pipelines.base_pipelines.py3.proxy import py3_proxy_subtree
from open_horadric.pipelines.base_pipelines.py3.server import py3_server_subtree
from open_horadric.pipelines.pipeline import PipelineTreeNode

config = Config()

py3_main_tree = PipelineTreeNode(
    converter=RootFolderConverter(folder_name="{}_{}".format(config.project_name, config.pipelines["py3"]["root_suffix"]))
)

py3_messages_subtree.children.append(py3_server_subtree)
py3_messages_subtree.children.append(py3_client_subtree)
py3_client_subtree.children.append(py3_proxy_subtree)
py3_main_tree.children.append(py3_messages_subtree)

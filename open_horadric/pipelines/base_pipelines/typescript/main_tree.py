# coding: utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from open_horadric.config.config import Config
from open_horadric.converters.root_folder.converter import RootFolderConverter
from open_horadric.dumpers.typescript.indexes_dumper import TypescriptIndexesDumper
from open_horadric.dumpers.typescript.package_info_dumper import PackageInfoDumper
from open_horadric.pipelines.base_pipelines.typescript.clients import typescript_clients_subtree
from open_horadric.pipelines.base_pipelines.typescript.interface import typescript_interfaces_subtree
from open_horadric.pipelines.base_pipelines.typescript.messages import typescript_messages_subtree
from open_horadric.pipelines.pipeline import PipelineTreeNode

config = Config()

typescript_main_tree = PipelineTreeNode(
    converter=RootFolderConverter(
        folder_name="{}_{}".format(config.project_name, config.pipelines["typescript"]["root_suffix"])
    ),
    dumpers=[TypescriptIndexesDumper()],
)

typescript_messages_subtree.children[0].children.append(typescript_clients_subtree)
typescript_interfaces_subtree.children[0].children.append(typescript_messages_subtree)
typescript_main_tree.children.append(typescript_interfaces_subtree)
typescript_main_tree.children.append(PipelineTreeNode(dumpers=[PackageInfoDumper()]))

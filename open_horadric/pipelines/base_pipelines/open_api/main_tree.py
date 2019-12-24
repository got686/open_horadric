from __future__ import annotations

from open_horadric.config.config import Config
from open_horadric.converters.root_folder.converter import RootFolderConverter
from open_horadric.dumpers.open_api.dumper import OpenApiDumper
from open_horadric.pipelines.pipeline import PipelineTreeNode

config = Config()


open_api_main_tree = PipelineTreeNode(
    converter=RootFolderConverter(folder_name="{}_{}".format(config.project_name, config.pipelines["open_api"]["root_suffix"])),
    dumpers=[OpenApiDumper()],
)

from __future__ import annotations

import os
from typing import Dict

from open_horadric.config.config import Config
from open_horadric.dumpers.base.jinja2_dumper import BaseJinja2Dumper
from open_horadric.dumpers.base.jinja2_dumper import OneWriteDict
from open_horadric.dumpers.typescript.imports import Exports
from open_horadric.dumpers.typescript.imports import Imports
from open_horadric.nodes.root import Root


class PackageInfoDumper(BaseJinja2Dumper):
    empty_imports = Imports()
    empty_exports = Exports()
    files_extension = "json"

    def dump(self, root: Root) -> Dict[str, str]:
        files = OneWriteDict()
        self.add_info(root=root, files=files)
        return files

    def add_services(self, root: Root, files: Dict[str, str]):
        pass

    def add_messages_and_enums(self, root: Root, files: Dict[str, str]):
        pass

    def add_info(self, root: Root, files: Dict[str, str]):
        config = Config()
        for file_name in ["package", "tsconfig"]:
            files[os.path.join(root.name, f"{file_name}.json")] = self.render(
                f"{file_name}.json.jinja2", context={"version": config.version, "root": root, "license": config.license}
            )

from __future__ import annotations

from copy import copy
from typing import Dict

from open_horadric.dumpers.base.jinja2_dumper import BaseJinja2Dumper
from open_horadric.dumpers.base.jinja2_dumper import OneWriteDict
from open_horadric.dumpers.typescript.imports import Export
from open_horadric.dumpers.typescript.imports import Exports
from open_horadric.dumpers.typescript.imports import Import
from open_horadric.dumpers.typescript.imports import Imports
from open_horadric.nodes.root import Root
from open_horadric.nodes.utils import walk_packages


class TypescriptIndexesDumper(BaseJinja2Dumper):
    empty_imports = Imports()
    empty_exports = Exports()
    files_extension = "ts"

    def dump(self, root: Root) -> Dict[str, str]:
        files = OneWriteDict()
        self.add_packages(root=root, files=files)
        return files

    def add_services(self, root: Root, files: Dict[str, str]):
        pass

    def add_messages_and_enums(self, root: Root, files: Dict[str, str]):
        pass

    def add_packages(self, root: Root, files: Dict[str, str]):
        for package in walk_packages(root):
            imports = copy(self.empty_imports)
            exports = copy(self.empty_exports)
            if package.name != "interfaces":  # TODO: fix this hack by pipeline
                names = []
                if package.messages:
                    names.append("interfaces")
                if package.messages or package.enums:
                    names.append("messages")
                if package.services:
                    names.append("clients")

                for subpackage in package.subpackages.values():
                    names.append(subpackage.name)

                for name in names:
                    imports.add_import(
                        Import(type_=Import.Type.LOCAL, import_name="*", import_from="./{}".format(name), import_as=name)
                    )

                    exports.add_import(Export(type_=Import.Type.LOCAL, import_name=name))

                files["/".join([p.name for p in package.full_namespace] + ["index.ts"])] = self.render(
                    "index.ts.jinja2", context={"imports": imports, "exports": exports}
                )

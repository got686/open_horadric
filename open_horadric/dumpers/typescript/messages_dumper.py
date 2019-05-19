from __future__ import annotations

from copy import copy
from typing import Dict

from open_horadric.dumpers.base.jinja2_dumper import BaseJinja2Dumper
from open_horadric.dumpers.base.jinja2_extensions import in_package
from open_horadric.dumpers.typescript.imports import Exports
from open_horadric.dumpers.typescript.imports import Import
from open_horadric.dumpers.typescript.imports import Imports
from open_horadric.nodes.package import Package
from open_horadric.nodes.root import Root
from open_horadric.nodes.utils import walk_packages


class TypescriptMessagesDumper(BaseJinja2Dumper):
    empty_imports = Imports()
    empty_exports = Exports()
    files_extension = "ts"

    def add_messages_and_enums(self, root: Root, files: Dict[str, str]) -> None:
        for package in walk_packages(package=root):
            if package.enums or package.messages:
                self.add_messages(package=package, files=files)
                pass

    def add_services(self, root: Root, files: Dict[str, str]) -> None:
        pass

    def add_messages(self, package: Package, files: Dict[str, str]) -> None:
        imports = copy(self.empty_imports)
        exports = copy(self.empty_exports)

        if package.messages:
            imports.add_import(
                Import(type_=Import.Type.LOCAL, import_name="*", import_from="./interfaces", import_as="interfaces")
            )

        for field_type in self.get_fields_types(package=package):
            if not in_package(field_type, package):
                imports.add_import(
                    Import(
                        type_=Import.Type.LOCAL,
                        import_name="*",
                        import_as=package.namespace[0].name,
                        import_from=package.namespace[0].name,
                    )
                )
                break

        context = {
            "imports": imports,
            "exports": exports,
            "messages": package.messages,
            "enums": package.enums,
            "package": package,
        }

        files[self.render_path(package=package)] = self.render("messages.ts.jinja2", context=context)

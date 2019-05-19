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


class TypescriptClientsDumper(BaseJinja2Dumper):
    empty_imports = Imports()
    empty_exports = Exports()
    files_extension = "ts"

    def add_messages_and_enums(self, root: Root, files: Dict[str, str]):
        pass

    def add_services(self, root: Root, files: Dict[str, str]):
        for package in walk_packages(package=root):
            if package.services:
                self.add_clients(package=package, files=files)

    def add_clients(self, package: Package, files: Dict[str, str]):
        imports = copy(self.empty_imports)
        exports = copy(self.empty_imports)

        imports.add_import(Import(type_=Import.Type.LIBRARY, import_name="AxiosInstance", import_from="axios"))

        imports.add_import(Import(type_=Import.Type.LIBRARY, import_name="AxiosResponse", import_from="axios"))

        import_root = False
        # TODO: remove import for request message
        for message in self.get_services_messages(package):
            if in_package(message, package):
                imports.add_import(
                    Import(type_=Import.Type.LOCAL, import_name=message.interface.root_class_name, import_from="./interfaces")
                )
                while not isinstance(message.parent, Package):  # for getting base message in package
                    message = message.parent

                imports.add_import(Import(type_=Import.Type.LOCAL, import_name=message.name, import_from="./messages"))
            else:
                import_root = True

        if import_root:
            imports.add_import(
                Import(
                    type_=Import.Type.LOCAL,
                    import_name="*",
                    import_from=package.namespace[0].name,
                    import_as=package.namespace[0].name,
                )
            )

        context = {"imports": imports, "exports": exports, "services": package.services, "package": package}

        files[self.render_path(package=package)] = self.render("client.ts.jinja2", context=context)

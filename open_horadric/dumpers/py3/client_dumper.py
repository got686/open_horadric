from __future__ import annotations

import logging
from copy import copy
from typing import Dict

from open_horadric.dumpers.base.jinja2_dumper import BaseJinja2Dumper
from open_horadric.dumpers.base.jinja2_extensions import in_package
from open_horadric.dumpers.base.jinja2_extensions import render_path
from open_horadric.dumpers.py3.imports import Import
from open_horadric.dumpers.py3.imports import Imports
from open_horadric.nodes.package import Package
from open_horadric.nodes.root import Root
from open_horadric.nodes.utils import walk_packages

logger = logging.getLogger("open_horadric.dumpers.py3_client")


class Py3ClientDumper(BaseJinja2Dumper):
    empty_imports = Imports()
    empty_imports.add_import(Import(type_=Import.Type.FUTURE, import_from="__future__", import_name="annotations"))
    files_extension = "py"

    def add_messages_and_enums(self, root: Root, files: Dict[str, str]):
        pass

    def add_services(self, root: Root, files: Dict[str, str]):
        for package in walk_packages(package=root):
            if package.services:
                self.add_clients(package=package, files=files)

    def add_clients(self, package: Package, files: Dict[str, str]):
        imports = copy(self.empty_imports)
        imports.add_import(Import(type_=Import.Type.CORE, import_name="logging"))
        imports.add_import(Import(type_=Import.Type.CORE, import_name="Any", import_from="typing"))
        imports.add_import(Import(type_=Import.Type.CORE, import_name="List", import_from="typing"))
        imports.add_import(Import(type_=Import.Type.LIBRARY, import_name="google.protobuf.empty_pb2"))
        imports.add_import(
            Import(type_=Import.Type.LIBRARY, import_name="BaseClient", import_from="open_horadric_lib.client.client")
        )

        self.add_services_imports(imports=imports, package=package)
        self.add_streaming_imports(imports=imports, package=package)

        context = {"imports": imports, "services": package.services, "package": package}

        files[self.render_path(package=package)] = self.render("client.py.jinja2", context=context)

    def add_services_imports(self, imports: Imports, package: Package):
        for message in self.get_services_messages(package=package):
            while not isinstance(message.parent, Package):  # for getting base message in package
                message = message.parent

            if in_package(message, package, exclude_root=True):
                imports.add_import(
                    Import(
                        type_=Import.Type.LOCAL, import_name=message.name, import_from=render_path(message.namespace.packages)
                    )
                )
            else:
                imports.add_import(Import(type_=Import.Type.LOCAL, import_name=render_path(message.namespace.packages)))

    @staticmethod
    def add_streaming_imports(imports: Imports, package: Package) -> None:
        for service in package.services.values():
            for method in service.methods.values():
                if method.multiple_input or method.multiple_output:
                    imports.add_import(Import(type_=Import.Type.CORE, import_name="Iterable", import_from="typing"))
                    return

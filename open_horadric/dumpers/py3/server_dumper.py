from __future__ import annotations

import logging
from copy import copy
from typing import Dict

from open_horadric.dumpers.py3.client_dumper import Py3ClientDumper
from open_horadric.dumpers.py3.imports import Import
from open_horadric.dumpers.py3.imports import Imports
from open_horadric.nodes.package import Package
from open_horadric.nodes.root import Root
from open_horadric.nodes.utils import walk_packages

logger = logging.getLogger("open_horadric.dumpers.packages")


class Py3ServerDumper(Py3ClientDumper):
    empty_imports = Imports()
    empty_imports.add_import(Import(type_=Import.Type.FUTURE, import_from="__future__", import_name="annotations"))
    files_extension = "py"

    def add_messages_and_enums(self, root: Root, files: Dict[str, str]):
        pass

    def add_services(self, root: Root, files: Dict[str, str]):
        for package in walk_packages(package=root):
            if package.services:
                self.add_servers(package=package, files=files)

    def add_servers(self, package: Package, files: Dict[str, str]):
        imports = copy(self.empty_imports)
        imports.add_import(Import(type_=Import.Type.LIBRARY, import_name="grpc"))
        imports.add_import(
            Import(type_=Import.Type.LIBRARY, import_name="RpcContext", import_from="grpc.framework.interfaces.face.face")
        )

        self.add_services_imports(imports=imports, package=package)
        self.add_streaming_imports(imports=imports, package=package)

        context = {"imports": imports, "services": package.services, "package": package}

        files[self.render_path(package=package)] = self.render("server.py.jinja2", context=context)

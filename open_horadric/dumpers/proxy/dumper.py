from __future__ import annotations

import os
from copy import copy
from typing import Dict

from open_horadric.converters.type_cast.py3.proxy import Py3Proxy
from open_horadric.dumpers.base.jinja2_extensions import render_path
from open_horadric.dumpers.py3.imports import Import
from open_horadric.dumpers.py3.server_dumper import Py3ServerDumper
from open_horadric.nodes.package import Package
from open_horadric.nodes.root import Root
from open_horadric.nodes.utils import walk_packages


class ProxyDumper(Py3ServerDumper):
    additional_templates = Py3ServerDumper.templates
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates")
    files_extension = "py"

    def __init__(self, cors: str):
        super().__init__()
        self.cors = cors

    def dump(self, root: Root) -> Dict[str, str]:
        files = super().dump(root=root)
        self.add_flask_app(root=root, files=files)
        return files

    def add_messages_and_enums(self, root: Root, files: Dict[str, str]) -> None:
        pass

    def add_services(self, root: Root, files: Dict[str, str]) -> None:
        for package in walk_packages(package=root):
            if package.services:
                self.add_proxy(package=package, files=files)

    def add_proxy(self, package: Package, files: Dict[str, str]):
        imports = copy(self.empty_imports)
        imports.add_import(Import(type_=Import.Type.CORE, import_name="logging"))
        imports.add_import(Import(type_=Import.Type.CORE, import_name="List", import_from="typing"))
        imports.add_import(Import(type_=Import.Type.LIBRARY, import_name="flask"))
        imports.add_import(
            Import(type_=Import.Type.LIBRARY, import_name="request", import_from="flask", import_as="flask_request")
        )
        imports.add_import(
            Import(type_=Import.Type.LIBRARY, import_name="BaseProxy", import_from="open_horadric_lib.proxy.proxy")
        )
        imports.add_import(
            Import(
                type_=Import.Type.LIBRARY,
                import_name="signature_types",
                import_from="open_horadric_lib.proxy.decorator.signature_types",
            )
        )
        imports.add_import(
            Import(
                type_=Import.Type.LIBRARY,
                import_name="BaseProxyMiddleware",
                import_from="open_horadric_lib.proxy.middleware.base",
            )
        )
        imports.add_import(
            Import(
                type_=Import.Type.LIBRARY,
                import_name="apply_middlewares",
                import_from="open_horadric_lib.proxy.middleware.base",
            )
        )
        imports.add_import(
            Import(type_=Import.Type.LIBRARY, import_name="Context", import_from="open_horadric_lib.base.context")
        )
        imports.add_import(
            Import(
                type_=Import.Type.LIBRARY, import_name="ErrorProcessor", import_from="open_horadric_lib.proxy.error_processor"
            )
        )
        imports.add_import(
            Import(type_=Import.Type.LIBRARY, import_name="Request", import_from="flask.wrappers", import_as="FlaskRequest")
        )

        for service in package.services.values():  # type: Py3Proxy
            imports.add_import(
                Import(
                    type_=Import.Type.LOCAL,
                    import_name=service.client.class_name,
                    import_from=render_path(service.client.namespace),
                )
            )

        self.add_services_imports(imports=imports, package=service.client.parent)

        context = {"imports": imports, "services": package.services, "package": package}

        files[self.render_path(package=package)] = self.render("proxy.py.jinja2", context=context)

    def add_flask_app(self, root: Root, files: Dict[str, str]):
        imports = copy(self.empty_imports)
        imports.add_import(Import(type_=Import.Type.LIBRARY, import_name="grpc"))
        imports.add_import(
            Import(type_=Import.Type.LIBRARY, import_name="ProxyApplication", import_from="open_horadric_lib.proxy.application")
        )
        imports.add_import(Import(type_=Import.Type.LIBRARY, import_name="CORS", import_from="flask_cors"))

        services = {}
        for package in walk_packages(package=root):
            if package.services:
                for service in package.services.values():
                    services[service.full_name] = service
                    imports.add_import(Import(type_=Import.Type.LOCAL, import_name=render_path(service.namespace)))
                    imports.add_import(Import(type_=Import.Type.LOCAL, import_name=render_path(service.client.namespace)))

        context = {"imports": imports, "services": services, "cors": self.cors}

        files["{}/flask_app.py".format(root.name)] = self.render("flask_app.py.jinja2", context=context)

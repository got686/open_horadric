from __future__ import annotations

import itertools
import logging
from copy import copy
from typing import Dict

from open_horadric.dumpers.base.jinja2_dumper import BaseJinja2Dumper
from open_horadric.dumpers.base.jinja2_extensions import in_package
from open_horadric.dumpers.base.jinja2_extensions import render_path
from open_horadric.dumpers.py3.imports import Import
from open_horadric.dumpers.py3.imports import Imports
from open_horadric.nodes.enum import Enum
from open_horadric.nodes.message import Message
from open_horadric.nodes.package import Package
from open_horadric.nodes.root import Root
from open_horadric.nodes.utils import walk_children
from open_horadric.nodes.utils import walk_packages

logger = logging.getLogger("open_horadric.dumpers.packages")


class Py3MessageDumper(BaseJinja2Dumper):
    empty_imports = Imports()
    empty_imports.add_import(Import(type_=Import.Type.FUTURE, import_from="__future__", import_name="annotations"))
    files_extension = "py"

    def add_messages_and_enums(self, root: Root, files: Dict[str, str]):
        for package in walk_packages(package=root):
            if package.enums or package.messages:
                self.add_messages_sources(package=package, files=files)
                self.add_messages_stubs(package=package, files=files)

    def add_messages_sources(self, package: Package, files: Dict[str, str]):
        imports = copy(self.empty_imports)

        for message in itertools.chain(package.messages.values(), package.enums.values()):
            imports.add_import(
                Import(
                    type_=Import.Type.LOCAL,
                    import_name=message.name,
                    import_from="{}_pb2".format(message.source_path.replace("/", ".")[: -len(".proto")]),
                )
            )

        context = {"imports": imports, "messages": package.messages, "enums": package.enums, "package": package}

        files[self.render_path(package=package)] = self.render("messages.py.jinja2", context=context)

    def add_messages_stubs(self, package: Package, files: Dict[str, str]):
        imports = copy(self.empty_imports)
        imports.add_import(Import(type_=Import.Type.LIBRARY, import_name="Message", import_from="google.protobuf.message"))

        import_scalar_list = False
        import_composite_list = False
        import_scalar_map = False
        import_composite_map = False
        imports_for_enum = False

        for child in walk_children(node=package):
            if isinstance(child, Enum):
                imports_for_enum = True
            elif isinstance(child, Message.Field):
                if child.container_type == Message.Field.ContainerType.LIST:
                    if child.type == Message.Field.Type.MESSAGE:
                        import_composite_list = True
                    else:
                        import_scalar_list = True
                elif child.container_type == Message.Field.ContainerType.MAP:
                    if child.type == Message.Field.Type.MESSAGE:
                        import_composite_map = True
                    else:
                        import_scalar_map = True

        for message in package.messages.values():
            if message.in_well_known_types:
                imports.add_import(
                    Import(
                        type_=Import.Type.LIBRARY,
                        import_name=message.name,
                        import_as="Protobuf{}".format(message.name),
                        import_from="google.protobuf.internal.well_known_types",
                    )
                )

        for import_name, check in {
            "RepeatedScalarFieldContainer": import_scalar_list,
            "RepeatedCompositeFieldContainer": import_composite_list,
            "ScalarMap": import_scalar_map,
            "MessageMap": import_composite_map,
        }.items():
            if check:
                imports.add_import(
                    Import(
                        type_=Import.Type.LIBRARY, import_name=import_name, import_from="google.protobuf.internal.containers"
                    )
                )

        for import_name, check in {
            "List": import_scalar_list or import_composite_list,
            "Dict": import_scalar_map or import_composite_map,
        }.items():
            if check:
                imports.add_import(Import(type_=Import.Type.CORE, import_name=import_name, import_from="typing"))

        if imports_for_enum:
            imports.add_import(Import(type_=Import.Type.CORE, import_name="List", import_from="typing"))
            imports.add_import(Import(type_=Import.Type.CORE, import_name="Tuple", import_from="typing"))

        for field_type in self.get_fields_types(package=package):
            if not in_package(field_type, package):
                imports.add_import(Import(type_=Import.Type.LOCAL, import_name=render_path(field_type.namespace.packages)))

        # messages.pyi rendering
        context = {"imports": imports, "messages": package.messages, "enums": package.enums, "package": package}

        files[self.render_path(package=package, file_extension="pyi")] = self.render("messages.pyi.jinja2", context=context)

    def add_services(self, root: Root, files: Dict[str, str]):
        pass

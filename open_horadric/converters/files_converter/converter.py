from __future__ import annotations

from copy import copy
from typing import Dict
from typing import Tuple
from typing import Type

from open_horadric.converters.base.converter import BaseConverter
from open_horadric.nodes.base import BaseNode
from open_horadric.nodes.enum import Enum
from open_horadric.nodes.index import NodesIndex
from open_horadric.nodes.message import Message
from open_horadric.nodes.namespace import Namespace
from open_horadric.nodes.package import Package
from open_horadric.nodes.root import Root
from open_horadric.nodes.service import Service
from open_horadric.nodes.utils import walk_children


class FilesConverter(BaseConverter):
    def __init__(self, type_file_map: Dict[Type[BaseNode] : str]):
        self.type_file_map = copy(type_file_map)
        self.path_package_map: Dict[Tuple[str, str], Package] = {}

    def convert(self, root: Root) -> Root:
        # index operations must be before links changes
        index = NodesIndex()
        index.root = root
        index.index()

        for child in walk_children(root):
            if type(child) in self.type_file_map:
                parent = child.parent
                new_package = self.get_or_create_package(child=child)
                child.namespace.insert_package(new_package)

                if isinstance(parent, Package):
                    if isinstance(child, Message):
                        new_package.messages[child.name] = child
                        del parent.messages[child.name]
                    elif isinstance(child, Enum):
                        new_package.enums[child.name] = child
                        del parent.enums[child.name]
                    elif isinstance(child, Service):
                        new_package.services[child.name] = child
                        del parent.services[child.name]
                    else:
                        raise ValueError("Bade child type: {} ({})".format(type(child), child))

        self.logger.info("Convert by %s result:\n%s", self, root.as_str(ident_level=1))
        return root

    def get_or_create_package(self, child: BaseNode):
        file_name = self.type_file_map[type(child)]
        package_key = (child.namespace.packages.path, file_name)

        if package_key not in self.path_package_map:
            new_package = Package(name=file_name, namespace=Namespace(child.namespace.packages), source_path="", extensions={})
            old_package = child.namespace.packages[-1]
            old_package.subpackages[new_package.name] = new_package

            self.path_package_map[package_key] = new_package

        return self.path_package_map[package_key]

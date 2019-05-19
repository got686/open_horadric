from __future__ import annotations

from typing import Callable
from typing import Dict
from typing import Optional

from open_horadric.converters.base.converter import BaseConverter
from open_horadric.nodes.index import NodesIndex
from open_horadric.nodes.package import Package
from open_horadric.nodes.root import Root
from open_horadric.nodes.utils import walk_children
from open_horadric.nodes.utils import walk_packages


class PackageRenameConverter(BaseConverter):
    def __init__(self, rule: Callable[[Package], Optional[str]]):
        self.rule = rule

    def convert(self, root: Root) -> Root:
        # index operations must be before links changes
        index = NodesIndex()
        index.root = root
        index.index()

        merge_map: Dict[Package, Package] = {}  # source -> target map
        for package in walk_packages(root):
            result_name = self.rule(package)
            if result_name is not None:
                # package merging if name exists
                if result_name in package.parent.subpackages:
                    merge_map[package] = package.parent.subpackages[result_name]
                else:
                    package.name = result_name

        for source, target in merge_map.items():
            del source.parent.subpackages[source.name]

            target.subpackages.update(source.subpackages)
            target.messages.update(source.messages)
            target.enums.update(source.enums)
            target.services.update(source.services)

            # TODO: fix all nested object namespace
            for item in source.children:
                for subitem in walk_children(item):
                    subitem.namespace[len(target.namespace)] = target

        self.logger.info("Convert by %s result:\n%s", self, root.as_str(ident_level=1))
        return root

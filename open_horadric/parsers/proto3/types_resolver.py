from __future__ import annotations

from open_horadric.base.indexer import ALL
from open_horadric.nodes.enum import Enum
from open_horadric.nodes.index import NodesIndex
from open_horadric.nodes.message import Message
from open_horadric.nodes.package import Package
from open_horadric.nodes.root import Root
from open_horadric.nodes.service import Service
from open_horadric.nodes.utils import walk_children


class TypesResolver:
    def resolve(self, root: Root):
        index = NodesIndex()
        index.root = root
        index.index()

        for child in walk_children(root):
            if isinstance(child, Message.Field):
                if child.type_name is not None:
                    child.type_obj = index.indexes[ALL]["{}.{}".format(root.name, child.type_name)]
            elif isinstance(child, Service.Method):
                child.input_obj = index.indexes[ALL]["{}.{}".format(root.name, child.input_name)]
                child.output_obj = index.indexes[ALL]["{}.{}".format(root.name, child.output_name)]
            elif isinstance(child, (Message, Service, Enum, Enum.Value, Package)):
                pass
            else:
                raise ValueError("Unknown type: %s (%s)", type(child), child)

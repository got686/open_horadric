from __future__ import annotations

from open_horadric.converters.base.converter import BaseConverter
from open_horadric.nodes.message import Message
from open_horadric.nodes.root import Root
from open_horadric.nodes.service import Service
from open_horadric.nodes.utils import walk_children

__all__ = ("RootFolderConverter", "NAME_TEMPLATE")


NAME_TEMPLATE = "{}.{}"


class RootFolderConverter(BaseConverter):
    def __init__(self, folder_name: str):
        self.folder_name = folder_name

    def convert(self, root: Root) -> Root:
        root.name = self.folder_name
        for child in walk_children(root):
            if isinstance(child, Service.Method):
                child.input_name = NAME_TEMPLATE.format(self.folder_name, child.input_name)
                child.output_name = NAME_TEMPLATE.format(self.folder_name, child.output_name)
            elif isinstance(child, Message.Field):
                if child.type_name is not None:
                    child.type_name = NAME_TEMPLATE.format(self.folder_name, child.type_name)
            else:
                pass

        self.logger.info("Convert by %s result:\n%s", self, root.as_str(ident_level=1))
        return root

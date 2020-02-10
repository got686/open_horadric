from __future__ import annotations

import inspect
import os
from abc import ABC
from typing import Any
from typing import Dict
from typing import Iterator
from typing import Union

from jinja2 import Environment
from jinja2 import FileSystemLoader
from open_horadric.dumpers.base.dumper import BaseDumper
from open_horadric.dumpers.base.imports import BaseImports
from open_horadric.dumpers.base.jinja2_extensions import node_to_str
from open_horadric.dumpers.base.jinja2_extensions import render_path
from open_horadric.dumpers.base.jinja2_extensions import to_snake_case
from open_horadric.nodes.enum import Enum
from open_horadric.nodes.message import Message
from open_horadric.nodes.package import Package
from open_horadric.nodes.root import Root
from open_horadric.nodes.utils import walk_children
from open_horadric.utils.classproperty import classproperty


class OneWriteDict(dict):
    def __setitem__(self, key, value):
        if key in self:
            raise ValueError("Key duplication {}".format(key))

        super().__setitem__(key, value)


class BaseJinja2Dumper(BaseDumper, ABC):
    additional_templates = ()
    empty_imports: BaseImports = None
    files_extension: str = None

    def __init__(self):
        super().__init__()
        self.logger.info("Dumper `%s` starts with templates: %s", self.__class__.__name__, self.templates)
        self.env: Environment = Environment(
            loader=FileSystemLoader(searchpath=self.templates), trim_blocks=True, lstrip_blocks=True
        )
        self.env.globals.update({"render_path": render_path, "to_snake_case": to_snake_case, "node_to_str": node_to_str})

    @classmethod
    def get_own_templates(cls):
        return os.path.join(os.path.dirname(os.path.abspath(inspect.getsourcefile(cls))), "templates")

    @classproperty
    def templates(self):
        return (self.get_own_templates(),) + self.additional_templates

    def dump(self, root: Root) -> Dict[str, str]:
        files: Dict[str, str] = OneWriteDict()
        self.add_messages_and_enums(root=root, files=files)
        self.add_services(root=root, files=files)
        return files

    def add_messages_and_enums(self, root: Root, files: Dict[str, str]) -> None:
        raise NotImplementedError

    def add_services(self, root: Root, files: Dict[str, str]) -> None:
        raise NotImplementedError

    def __init_subclass__(cls, **kwargs):
        if cls.templates is None:
            raise ValueError("`templates` must be set")

        if cls.empty_imports is None:
            raise ValueError("`empty_imports` must be set")

        if cls.files_extension is None:
            raise ValueError("`files_extension` must be set")

        super().__init_subclass__(**kwargs)

    @classmethod
    def _get_own_templates(cls):
        return os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(cls))), "templates")

    def render(self, template_name: str, context: Dict[str, Any] = None) -> str:
        if context is None:
            context = {}

        if "imports" not in context:
            context["imports"] = self.empty_imports

        template = self.env.get_template(name=template_name)
        content = template.render(context)

        return content

    def render_path(self, package: Package, file_extension: str = None) -> str:
        # os.path.join with '\' on windows does not works in protobuf
        if file_extension is None:
            file_extension = self.files_extension
        return "{}.{}".format(render_path(path=package.full_namespace, delimiter="/"), file_extension)

    @staticmethod
    def get_services_messages(package: Package) -> Iterator[Message]:
        for service in package.services.values():
            for method in service.methods.values():
                for message in (method.input_obj, method.output_obj):
                    yield message

    @staticmethod
    def get_fields_types(package: Package) -> Iterator[Union[Message, Enum]]:
        for child in walk_children(node=package):
            if isinstance(child, Message.Field):
                if child.type_obj is not None:
                    yield child.type_obj

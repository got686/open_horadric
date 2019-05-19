from __future__ import annotations

from typing import Dict

from open_horadric.converters.type_cast.converter import fix_method
from open_horadric.converters.type_cast.converter import fix_service
from open_horadric.converters.type_cast.py3.client import Py3Client
from open_horadric.dumpers.base.jinja2_extensions import render_path
from open_horadric.nodes.base import BaseNode
from open_horadric.nodes.base import ExtensionsType
from open_horadric.nodes.namespace import Namespace


class Py3Proxy(Py3Client):
    def __init__(self, name: str, namespace: Namespace, source_path: str, extensions: ExtensionsType):
        super().__init__(name, namespace, source_path, extensions)
        self.client: Py3Client = None

    @property
    def class_name(self) -> str:
        return "{}Proxy".format(self.name)

    @property
    def no_root_name(self) -> str:
        return render_path(self.namespace[1:-1] + [self.name])


def fix_proxy_service(target: Py3Proxy, source: Py3Client, source_target_map: Dict[BaseNode, BaseNode]):
    fix_service(target=target, source=source, source_target_map=source_target_map)
    target.client = source


def fix_proxy_method(target: Py3Proxy.Method, source: Py3Client.Method, source_target_map: Dict[BaseNode, BaseNode]):
    fix_method(target=target, source=source, source_target_map=source_target_map)
    target.input_obj = source.input_obj
    target.output_obj = source.output_obj

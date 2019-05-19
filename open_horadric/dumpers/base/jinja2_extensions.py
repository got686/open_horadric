from __future__ import annotations

import logging
import re
from typing import Iterable
from typing import List
from typing import Union

from open_horadric.nodes.base import BaseNode
from open_horadric.nodes.package import Package

logger = logging.getLogger("jinja2_extensions")


def render_path(path: Iterable[Union[BaseNode, str]], delimiter: str = "."):
    return delimiter.join([p.name if isinstance(p, BaseNode) else p for p in path])


def to_snake_case(string: str):
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", string)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def to_camel_case(string: str):
    parts = string.split("_")
    return "".join([parts[0]] + [p.capitalize() for p in parts[1:]])


def to_pascal_case(string: str):
    parts = string.split("_")
    return "".join(p[0].capitalize() + p[1:] for p in parts if p)


def in_same_package(left_node: BaseNode, right_node: BaseNode, exclude_root: bool = False) -> bool:
    left_packages = left_node.namespace.packages
    right_packages = right_node.namespace.packages
    if len(left_packages) != len(right_packages):
        return False

    if exclude_root:
        compare_slice = slice(1, -1)
    else:
        compare_slice = slice(-1)

    return all(l.name == r.name for l, r in zip(left_packages[compare_slice], right_packages[compare_slice]))


def in_package(node: BaseNode, package: Package, exclude_root: bool = False):
    left_packages = node.namespace.packages
    right_packages = package.full_namespace.packages
    if len(left_packages) != len(right_packages):
        return False

    if exclude_root:
        compare_slice = slice(1, -1)
    else:
        compare_slice = slice(-1)
    return all(l.name == r.name for l, r in zip(left_packages[compare_slice], right_packages[compare_slice]))


def get_path(node: BaseNode, namespace: List[BaseNode] = None, file_name=None) -> List[Union[BaseNode, str]]:
    packages = node.namespace.packages

    if namespace is None:
        if file_name is None:
            path = node.namespace
        else:
            path = packages + [file_name] + node.namespace[len(node.namespace.packages) :]
    else:
        if packages == namespace[: len(packages)]:
            path = node.namespace[len(packages) :]
        else:
            if file_name is None:
                path = node.namespace
            else:
                path = node.namespace.packages + [file_name] + node.namespace[len(packages) :]

    return path


def node_to_str(node: BaseNode, namespace: List[BaseNode] = None, delimiter=".", file_name=None):
    path = get_path(node=node, namespace=namespace, file_name=file_name)

    return render_path(path=path + [node], delimiter=delimiter)

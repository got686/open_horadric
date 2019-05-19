from __future__ import annotations

from typing import Iterator
from typing import Union

from open_horadric.nodes.base import BaseNode
from open_horadric.nodes.enum import Enum
from open_horadric.nodes.message import Message
from open_horadric.nodes.package import Package
from open_horadric.nodes.service import Service

__all__ = (
    "walk_children",
    "walk_packages",
    "walk_messages",
    "walk_fields",
    "walk_services",
    "walk_methods",
    "walk_enums",
    "walk_enum_values",
)


def walk_children(node: BaseNode) -> Iterator[BaseNode]:
    return _walk_children(node=node)


def _walk_children(node: BaseNode) -> Iterator[BaseNode]:
    yield node
    for child in node.children:
        for inner_child in _walk_children(node=child):
            yield inner_child


def walk_packages(package: Package) -> Iterator[Package]:
    return _walk_subpackages(package=package)


def _walk_subpackages(package: Package) -> Iterator[Package]:
    yield package
    for subpackage in package.subpackages.values():
        for inner_package in _walk_subpackages(package=subpackage):
            yield inner_package


def walk_messages(package: Package) -> Iterator[Message]:
    for subpackage in walk_packages(package=package):
        for message in _walk_messages(parent=subpackage):
            yield message


def _walk_messages(parent: Union[Package, Message]) -> Iterator[Message]:
    for message in parent.messages.values():
        yield message
        for child in message.messages.values():
            yield child


def walk_fields(package: Package) -> Iterator[Message.Field]:
    for message in walk_messages(package=package):
        for field in message.fields.values():
            yield field


def walk_services(package: Package) -> Iterator[Service]:
    for subpackage in walk_packages(package=package):
        for service in subpackage.services.values():
            yield service


def walk_methods(package: Package) -> Iterator[Service.Method]:
    for service in walk_services(package=package):
        for method in service.methods.values():
            yield method


def walk_enums(package: Package) -> Iterator[Enum]:
    for subpackage in walk_packages(package=package):
        for enum in subpackage.enums.values():
            yield enum

        for message in walk_messages(package=subpackage):
            for enum in message.enums.values():
                yield enum


def walk_enum_values(package: Package) -> Iterator[Enum.Value]:
    for enum in walk_enums(package=package):
        for value in enum.values.values():
            yield value

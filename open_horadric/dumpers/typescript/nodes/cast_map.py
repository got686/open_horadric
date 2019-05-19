from __future__ import annotations

from open_horadric.dumpers.typescript.nodes.enum import TypescriptEnum
from open_horadric.dumpers.typescript.nodes.message import TypescriptMessage
from open_horadric.dumpers.typescript.nodes.package import TypescriptPackage
from open_horadric.dumpers.typescript.nodes.service import TypescriptService
from open_horadric.nodes.enum import Enum
from open_horadric.nodes.message import Message
from open_horadric.nodes.package import Package
from open_horadric.nodes.root import Root
from open_horadric.nodes.service import Service

typescript_cast_map = {
    Root: Root,
    Package: TypescriptPackage,
    Message: TypescriptMessage,
    Message.Field: TypescriptMessage.Field,
    Enum: TypescriptEnum,
    Enum.Value: TypescriptEnum.Value,
    Service: TypescriptService,
    Service.Method: TypescriptService.Method,
}

from __future__ import annotations

from typing import Dict
from typing import Type
from typing import TypeVar

from open_horadric.nodes.base import BaseNode
from open_horadric.nodes.base import ExtensionsType
from open_horadric.nodes.message import Message
from open_horadric.nodes.namespace import Namespace


class Service(BaseNode):
    class Method(BaseNode):
        def __init__(self, name: str, namespace: Namespace, source_path: str, extensions: ExtensionsType):
            super().__init__(name, namespace, source_path, extensions)
            self.input_name: str = None
            self.output_name: str = None
            self.multiple_input: bool = False
            self.multiple_output: bool = False
            self.input_obj: Message = None
            self.output_obj: Message = None

        def _body_as_str(self, ident_level):
            return "{ident}<{class_name}({name} {input_name}=>{output_name} id='{id}')>".format(
                ident="\t" * ident_level,
                class_name=self.__class__.__name__,
                name=self.name,
                input_name=self.input_obj.full_name,
                output_name=self.output_obj.full_name,
                id=id(self),
            )

        def cast_to(self, target_class: Type[ServiceMethodType]) -> ServiceMethodType:
            if not issubclass(target_class, Service.Method):
                raise ValueError("`target_class` must be a subclass of `Service.Method`")

            return target_class(
                name=self.name, namespace=self.namespace, source_path=self.source_path, extensions=self.extensions
            )

    def __init__(self, name: str, namespace: Namespace, source_path: str, extensions: ExtensionsType):
        super().__init__(name, namespace, source_path, extensions)
        self.methods: Dict[str, Service.Method] = {}

    @property
    def children(self):
        return list(self.methods.values())

    def cast_to(self, target_class: Type[ServiceType]) -> ServiceType:
        if not issubclass(target_class, Service):
            raise ValueError("`target_class` must be a subclass of `Service`")

        return target_class(name=self.name, namespace=self.namespace, source_path=self.source_path, extensions=self.extensions)


ServiceType = TypeVar("ServiceType", bound=Service)
ServiceMethodType = TypeVar("ServiceMethodType", bound=Service.Method)

from __future__ import annotations

from open_horadric.converters.type_cast.typescript.interface import TypescriptMessageInterface
from open_horadric.dumpers.base.jinja2_extensions import in_same_package
from open_horadric.dumpers.base.jinja2_extensions import render_path
from open_horadric.dumpers.base.jinja2_extensions import to_camel_case
from open_horadric.nodes.service import Service


class TypescriptClient(Service):
    class Method(Service.Method):
        @property
        def input_interface_string(self) -> str:
            interface = self.input_obj.interface  # type: TypescriptMessageInterface
            if in_same_package(self, interface):
                return interface.root_class_name
            else:
                return render_path(interface.namespace + [interface.root_class_name])

        @property
        def output_interface_string(self) -> str:
            interface = self.output_obj.interface  # type: TypescriptMessageInterface
            if in_same_package(self, interface):
                return interface.root_class_name
            else:
                return render_path(interface.namespace + [interface.root_class_name])

        @property
        def output_type_string(self) -> str:
            obj = self.output_obj
            if in_same_package(self, obj):
                return render_path(obj.namespace.other + [obj.name])
            else:
                return render_path(obj.namespace + [obj.name])

        @property
        def name_string(self) -> str:
            return to_camel_case(self.name)

    @property
    def class_name(self) -> str:
        return "{}Client".format(self.name)

    @property
    def grpc_path_string(self) -> str:
        return render_path(self.namespace[1:-1] + [self])

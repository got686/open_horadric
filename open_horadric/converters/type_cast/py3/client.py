from __future__ import annotations

from open_horadric.dumpers.base.jinja2_extensions import in_same_package
from open_horadric.dumpers.base.jinja2_extensions import render_path
from open_horadric.nodes.service import Service


class Py3Client(Service):
    @property
    def class_name(self) -> str:
        return "{}Client".format(self.name)

    @property
    def full_class_name(self):
        return render_path(self.namespace + [self.class_name])

    @property
    def grpc_path_string(self) -> str:
        return render_path(self.namespace[1:-1] + [self])

    class Method(Service.Method):
        @property
        def input_string(self) -> str:
            if in_same_package(self, self.input_obj, exclude_root=True):
                return render_path(self.input_obj.full_namespace.other)
            else:
                return render_path(self.input_obj.full_namespace)

        @property
        def output_string(self) -> str:
            if in_same_package(self, self.output_obj, exclude_root=True):
                return render_path(self.output_obj.full_namespace.other)
            else:
                return render_path(self.output_obj.full_namespace)

        @property
        def input_type_string(self) -> str:
            if not self.multiple_input:
                return self.input_string

            return "Iterable[{}]".format(self.input_string)

        @property
        def output_type_string(self) -> str:
            if not self.multiple_output:
                return self.output_string

            return "Iterable[{}]".format(self.output_string)

        @property
        def handler_name_string(self) -> str:
            _input = "stream" if self.multiple_input else "unary"
            _output = "stream" if self.multiple_output else "unary"
            return "{}_{}".format(_input, _output)

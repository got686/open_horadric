from __future__ import annotations

from open_horadric.converters.type_cast.py3.client import Py3Client


class Py3Server(Py3Client):
    @property
    def class_name(self):
        return "{}Interface".format(self.name)

    class Method(Py3Client.Method):
        @property
        def handler_name_string(self) -> str:
            return "{}_rpc_method_handler".format(super().handler_name_string)

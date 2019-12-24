from __future__ import annotations

import copy
from typing import Dict

import yaml
from open_horadric.dumpers.base.dumper import BaseDumper
from open_horadric.dumpers.base.jinja2_extensions import render_path
from open_horadric.nodes.message import Message
from open_horadric.nodes.root import Root
from open_horadric.nodes.utils import walk_enums
from open_horadric.nodes.utils import walk_messages
from open_horadric.nodes.utils import walk_methods

BASE_STRUCTURE = {
    "openapi": "3.0.0",
    "components": {"schemas": {}},
    "paths": {},
    "info": {"version": "1.0.0", "title": "Some title"},
}


FIELDS_TYPES_MAP = {
    Message.Field.Type.DOUBLE: "number",
    Message.Field.Type.FLOAT: "number",
    Message.Field.Type.INT64: "integer",
    Message.Field.Type.UINT64: "integer",
    Message.Field.Type.INT32: "integer",
    Message.Field.Type.FIXED64: "integer",
    Message.Field.Type.FIXED32: "integer",
    Message.Field.Type.BOOL: "boolean",
    Message.Field.Type.STRING: "string",
    Message.Field.Type.BYTES: "string",  # TODO: find specific typescript bytes field
    Message.Field.Type.UINT32: "integer",
    Message.Field.Type.SFIXED32: "integer",
    Message.Field.Type.SFIXED64: "integer",
    Message.Field.Type.SINT32: "integer",
    Message.Field.Type.SINT64: "integer",
}

FIELDS_FORMATS_MAP = {
    Message.Field.Type.DOUBLE: "double",
    Message.Field.Type.FLOAT: "double",
    Message.Field.Type.INT64: "int64",
    Message.Field.Type.UINT64: "int64",
    Message.Field.Type.INT32: "int32",
    Message.Field.Type.FIXED64: "int64",
    Message.Field.Type.FIXED32: "int32",
    Message.Field.Type.UINT32: "int32",
    Message.Field.Type.SFIXED32: "int32",
    Message.Field.Type.SFIXED64: "int64",
    Message.Field.Type.SINT32: "int32",
    Message.Field.Type.SINT64: "int64",
}


class OpenApiDumper(BaseDumper):
    def dump(self, root: Root) -> Dict[str, str]:
        structure = copy.deepcopy(BASE_STRUCTURE)
        structure["components"]["schemas"] = self.make_components(root=root)
        structure["paths"] = self.make_paths(root=root)

        return {"open_api.yaml": yaml.dump(structure)}

    @staticmethod
    def make_components(root: Root) -> Dict:
        structures = {}

        for enum in walk_enums(root):
            values = []
            for value in enum.values.values():
                values.append(value.name)

            structures[enum.full_name] = {"type": "string", "enum": values}

        for message in walk_messages(root):
            properties = {}
            for field in message.fields.values():
                if field.type in {Message.Field.Type.MESSAGE, Message.Field.Type.ENUM}:
                    ref = f"#/components/schemas/{field.type_obj.full_name}"
                    if field.container_type == field.ContainerType.LIST:
                        field_description = {"type": "array", "items": ref}
                    elif field.container_type == field.ContainerType.MAP:
                        field_description = {"type": "object", "additionalProperties": {"$ref": ref}}
                    else:
                        field_description = {"$ref": ref}
                else:
                    field_description = {"type": FIELDS_TYPES_MAP[field.type]}  # FIXME
                    if field.type == Message.Field.Type.BOOL:
                        field_description["default"] = False
                    elif field.type in {Message.Field.Type.STRING, Message.Field.Type.BYTES}:
                        field_description["default"] = ""
                    else:
                        field_description["default"] = 0

                    if field.type in FIELDS_FORMATS_MAP:
                        field_description["format"] = FIELDS_FORMATS_MAP[field.type]

                    if field.type in {Message.Field.Type.UINT32, Message.Field.Type.UINT64}:
                        field_description["minimum"] = 0

                properties[field.name] = field_description

            structures[message.full_name] = {"type": "object", "properties": properties}

        return structures

    @staticmethod
    def make_paths(root: Root) -> Dict:
        paths = {}

        for method in walk_methods(root):
            path = {
                "operationId": method.full_name,
                "requestBody": {
                    "content": {"application/json": {"schema": {"$ref": f"#/components/schemas/{method.input_obj.full_name}"}}}
                },
                "responses": {
                    "200": {
                        "description": "Some description",
                        "content": {
                            "application/json": {"schema": {"$ref": f"#/components/schemas/{method.output_obj.full_name}"}}
                        },
                    }
                },
            }

            paths[f"/{ render_path(method.namespace[1:-1]) }/{ method.name }"] = {"post": path}

        return paths

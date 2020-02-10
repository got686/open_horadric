#!/usr/bin/env python

"""
Python script which must receive data from protoc binary to input and write data for generating files to output.
"""

from __future__ import annotations

import logging
import os
import sys

from google.protobuf.compiler import plugin_pb2

from open_horadric.config.config import Config
from open_horadric.parsers.proto3.source import FileSource
from open_horadric.pipelines.base_pipelines.py3.pipeline import py3_pipeline
from open_horadric.pipelines.base_pipelines.typescript.pipeline import typescript_pipeline

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


handler = logging.FileHandler("plugin.log")
handler.setLevel(logging.INFO)
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(handler)


def generate_response(request):
    response = plugin_pb2.CodeGeneratorResponse()
    sources = [FileSource.from_descriptor(file_descriptor) for file_descriptor in request.proto_file]

    for pipeline in (py3_pipeline, typescript_pipeline):
        for path, source in pipeline.run(sources=sources).items():
            f = response.file.add()
            f.name = path
            f.content = source

    return response


def run_plugin(func):
    config = Config()

    data = sys.stdin.buffer.read()
    if config.debug:
        with open("debug_data_dump", "wb+") as f:
            f.write(data)

    plugin_request = plugin_pb2.CodeGeneratorRequest()
    plugin_request.ParseFromString(data)
    plugin_response = func(plugin_request)
    output = plugin_response.SerializeToString()

    sys.stdout.buffer.write(output)


if __name__ == "__main__":
    run_plugin(generate_response)

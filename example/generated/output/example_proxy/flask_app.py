"""
Generated by open_horadric. DO NOT EDIT!
"""

from __future__ import annotations

from flask_cors import CORS
from open_horadric_lib.proxy.application import ProxyApplication
from open_horadric_lib.proxy.middleware.protocol_converter import ProtocolConverterMiddleware
import grpc

import example_proxy.foo.bar.proxy
import example_py3.foo.bar.client

app = ProxyApplication('py3_proxy')
cors = CORS(app, resources={r"/*": {"origins": "*"}})
channel = grpc.insecure_channel('localhost:50051')

example_proxy.foo.bar.proxy.TestServiceProxy(
    client=example_py3.foo.bar.client.TestServiceClient(channel=channel),
    middlewares=[ProtocolConverterMiddleware()]
).bind(app=app)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080)
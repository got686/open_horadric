"""
Generated by open_horadric. DO NOT EDIT!
"""

from __future__ import annotations

from typing import List
import logging

from flask import request as flask_request
from horadric_lib.proxy.decorator.signature_types import signature_types
from horadric_lib.proxy.middleware.base import apply_middlewares
from horadric_lib.proxy.middleware.base import BaseProxyMiddleware
from horadric_lib.proxy.proxy import BaseProxy
import flask

from example_py3.foo.bar.client import TestServiceClient
from example_py3.foo.bar.messages import TestMessage
import example_py3.google.protobuf.messages


class TestServiceProxy(BaseProxy):
    """
    Proxy-converter to grpc for example_proxy.foo.bar.proxy.TestService.
    """

    logger = logging.getLogger('example_proxy.foo.bar.proxy.TestService')

    def __init__(self, client: TestServiceClient, middlewares: List[BaseProxyMiddleware]):
        super().__init__(client, middlewares)

    def test_method(
            self,
            request: TestMessage
    ) -> TestMessage.TestNestedMessage:
        return self.client.test_method(request)

    def client_streaming(
            self,
            request: TestMessage
    ) -> TestMessage.TestNestedMessage:
        return self.client.client_streaming(request)

    def server_streaming(
            self,
            request: TestMessage
    ) -> TestMessage.TestNestedMessage:
        return self.client.server_streaming(request)

    def client_server_streaming(
            self,
            request: TestMessage.TestNestedMessage
    ) -> TestMessage.TestNestedMessage:
        return self.client.client_server_streaming(request)

    def empty_method(
            self,
            request: example_py3.google.protobuf.messages.Empty
    ) -> example_py3.google.protobuf.messages.Empty:
        return self.client.empty_method(request)

    @signature_types(TestMessage, TestMessage.TestNestedMessage)
    def _test_method(self) -> TestMessage.TestNestedMessage:
        return self.test_method(flask_request)

    @signature_types(TestMessage, TestMessage.TestNestedMessage)
    def _client_streaming(self) -> TestMessage.TestNestedMessage:
        return self.client_streaming(flask_request)

    @signature_types(TestMessage, TestMessage.TestNestedMessage)
    def _server_streaming(self) -> TestMessage.TestNestedMessage:
        return self.server_streaming(flask_request)

    @signature_types(TestMessage.TestNestedMessage, TestMessage.TestNestedMessage)
    def _client_server_streaming(self) -> TestMessage.TestNestedMessage:
        return self.client_server_streaming(flask_request)

    @signature_types(example_py3.google.protobuf.messages.Empty, example_py3.google.protobuf.messages.Empty)
    def _empty_method(self) -> example_py3.google.protobuf.messages.Empty:
        return self.empty_method(flask_request)

    def bind(self, app: flask.Flask):
        self.test_method = apply_middlewares(self.test_method, *self.middlewares)

        app.add_url_rule(
            rule='/foo.bar.TestService/TestMethod',
            view_func=self._test_method,
            methods=('POST', 'GET'),
            endpoint='foo.bar.TestService/TestMethod',
        )

        self.client_streaming = apply_middlewares(self.client_streaming, *self.middlewares)

        app.add_url_rule(
            rule='/foo.bar.TestService/ClientStreaming',
            view_func=self._client_streaming,
            methods=('POST', 'GET'),
            endpoint='foo.bar.TestService/ClientStreaming',
        )

        self.server_streaming = apply_middlewares(self.server_streaming, *self.middlewares)

        app.add_url_rule(
            rule='/foo.bar.TestService/ServerStreaming',
            view_func=self._server_streaming,
            methods=('POST', 'GET'),
            endpoint='foo.bar.TestService/ServerStreaming',
        )

        self.client_server_streaming = apply_middlewares(self.client_server_streaming, *self.middlewares)

        app.add_url_rule(
            rule='/foo.bar.TestService/ClientServerStreaming',
            view_func=self._client_server_streaming,
            methods=('POST', 'GET'),
            endpoint='foo.bar.TestService/ClientServerStreaming',
        )

        self.empty_method = apply_middlewares(self.empty_method, *self.middlewares)

        app.add_url_rule(
            rule='/foo.bar.TestService/EmptyMethod',
            view_func=self._empty_method,
            methods=('POST', 'GET'),
            endpoint='foo.bar.TestService/EmptyMethod',
        )


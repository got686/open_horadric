"""
Generated by open_horadric. DO NOT EDIT!
"""

from __future__ import annotations

from google.protobuf.message import Message

__all__ = ('Empty',)


class Empty(Message):
    def __init__(
            self,
    ) -> None: ...

    @classmethod
    def FromString(cls, s: bytes) -> Empty: ...
    def MergeFrom(self, other_msg: Message) -> None: ...
    def CopyFrom(self, other_msg: Message) -> None: ...
    def HasField(self, field_name: str) -> bool: ...
    def ClearField(self, field_name: str) -> None: ...
    def WhichOneof(self, oneof_group: str) -> str: ...
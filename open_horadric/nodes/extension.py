from __future__ import annotations

from typing import Union


# TODO: it must be subclass of some BaseNode subclasses
class BaseExtension:
    def __init__(self, name: str, value: Union[str, int, float]):
        self.name = name
        self.value = value

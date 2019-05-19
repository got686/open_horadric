from __future__ import annotations

from typing import List

from open_horadric.nodes.root import Root
from open_horadric.parsers.base.source import BaseSource


class BaseParser:
    def parse(self, sources: List[BaseSource]) -> Root:
        raise NotImplementedError

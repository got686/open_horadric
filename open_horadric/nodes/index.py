from __future__ import annotations

from typing import Dict
from typing import List
from typing import Type
from typing import TypeVar
from typing import Union

from open_horadric.base.indexer import BaseTreeIndexer
from open_horadric.nodes.base import BaseNode
from open_horadric.nodes.root import Root

NodeObject = TypeVar("NodeObject", bound=BaseNode)


class NodesIndexer(BaseTreeIndexer):
    get_children_map = {}

    def get_path_str(self, obj: BaseNode, path: List[BaseNode]) -> str:
        return ".".join(part.name for part in obj.namespace + [obj])

    @classmethod
    def get_children(cls, obj: BaseNode):
        return obj.children or ()


class NodesIndex:
    def __init__(self):
        self._root = None
        self._indexer = NodesIndexer()
        self.indexes: Dict[Union[str, Type[NodeObject]], Dict[str, NodeObject]] = None

    def index(self):
        if self._root is None:
            raise ValueError("You must set `Root` node before index process")

        self.indexes = self._indexer.index(objs=[self._root])

    @property
    def root(self):
        return self.root

    @root.setter
    def root(self, root: Root):
        self._root = root

    def clear(self):
        self._root = None
        self.indexes = None

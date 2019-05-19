from __future__ import annotations

import logging
from collections import defaultdict
from typing import Callable
from typing import DefaultDict
from typing import Dict
from typing import Iterable
from typing import List
from typing import Type
from typing import TypeVar
from typing import Union

ObjectsClassType = TypeVar("ObjectsClassType")
IndexesType = DefaultDict[Union[str, Type[ObjectsClassType]], Dict[str, ObjectsClassType]]

ALL = "__all__"

logger = logging.getLogger("open_horadric.base.indexer")


class BaseTreeIndexer:
    get_children_map: Dict[Union[str, ObjectsClassType], Callable[[ObjectsClassType], Iterable[ObjectsClassType]]] = None

    def __init_subclass__(cls, **kwargs):
        if cls.get_children_map is None:
            raise ValueError("`get_children_map` must be set on subclass")

        super().__init_subclass__(**kwargs)

    def index(self, objs: Iterable[ObjectsClassType]) -> IndexesType:
        indexes = defaultdict(dict)
        for obj in objs:
            self._index(obj=obj, indexes=indexes, path=[obj])

        return indexes

    def _index(self, obj: ObjectsClassType, indexes: IndexesType, path: List[ObjectsClassType]):
        path_str = self.get_path_str(obj=obj, path=path)

        indexes[ALL][path_str] = obj
        indexes[type(obj)][path_str] = obj
        for child in self.get_children(obj=obj):
            # Optimization for O(n)
            child_path = path
            child_path.append(child)

            self._index(obj=child, indexes=indexes, path=path)
            child_path.pop()

    def get_path_str(self, obj: ObjectsClassType, path: List[ObjectsClassType]) -> str:
        raise NotImplementedError

    @classmethod
    def get_children(cls, obj: ObjectsClassType) -> Iterable[ObjectsClassType]:
        return cls.get_children_map[type(obj)](obj)

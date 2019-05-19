from __future__ import annotations

import inspect
import logging
import os
from typing import Dict

from open_horadric.nodes.root import Root
from open_horadric.utils.classproperty import classproperty


class BaseDumper:
    static_files = ()
    logger = logging.getLogger("open_horadric.dumper")

    def dump(self, root: Root) -> Dict[str, str]:
        raise NotImplementedError

    @classmethod
    def _get_own_static_files(cls):
        return os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(cls))), "static")

    @classproperty
    def static_files(self):
        return (self._get_own_static_files(),) + self.static_files

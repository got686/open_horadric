from __future__ import annotations

import logging

from open_horadric.nodes.root import Root


class BaseConverter:
    logger = logging.getLogger("open_horadric.converter")

    def convert(self, root: Root) -> Root:
        raise NotImplementedError

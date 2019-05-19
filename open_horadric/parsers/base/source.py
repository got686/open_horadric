from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class BaseSource:
    path: str
    content: Any
    source_content: str

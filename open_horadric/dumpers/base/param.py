from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class BaseParam:
    name: str
    value: Any
    value_type: Any

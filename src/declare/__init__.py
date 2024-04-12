from __future__ import annotations
from typing import Type
from ._declare import Declare as Declare

__all__ = [
    "Declare",
    "Int",
    "Float",
    "Bool",
    "Str",
    "Bytes",
]

Int: Type[Declare[int]] = Declare
Float: Type[Declare[float]] = Declare
Bool: Type[Declare[bool]] = Declare
Str: Type[Declare[str]] = Declare
Bytes: Type[Declare[bytes]] = Declare

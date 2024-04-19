from __future__ import annotations

from ._declare import Declare as Declare

__all__ = [
    "Declare",
    "Int",
    "Float",
    "Bool",
    "Str",
    "Bytes",
]

Int: type[Declare[int]] = Declare
Float: type[Declare[float]] = Declare
Bool: type[Declare[bool]] = Declare
Str: type[Declare[str]] = Declare
Bytes: type[Declare[bytes]] = Declare

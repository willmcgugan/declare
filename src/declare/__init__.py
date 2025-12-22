from __future__ import annotations
from typing import TypeVar

from ._declare import Declare as Declare
from ._declare import init as init
from ._declare import watch as watch
from ._declare import ValueType

__all__ = [
    "Declare",
    "Int",
    "Float",
    "Bool",
    "Str",
    "Bytes",
    "List",
    "Tuple",
    "Set",
    "Dict",
    "watch",
]

Int: type[Declare[int]] = Declare
Float: type[Declare[float]] = Declare
Bool: type[Declare[bool]] = Declare
Str: type[Declare[str]] = Declare
Bytes: type[Declare[bytes]] = Declare


KeyType = TypeVar("KeyType")


class List(Declare[list[ValueType]]):
    """Declare a list attribute."""


class Tuple(Declare[tuple[ValueType]]):
    """Declare a tuple attribute."""


class Set(Declare[tuple[ValueType]]):
    """Declare a set attribute."""


class Dict(Declare[dict[KeyType, ValueType]]):
    """Declare a dict attribute."""

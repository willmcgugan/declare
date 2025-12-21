from typing import List

import declare
from declare import Declare, watch


def test_predefined():
    class Foo:
        my_int = declare.Int(1)
        my_float = declare.Float(3.14)
        my_bool = declare.Bool(True)
        my_str = declare.Str("Foo")
        my_bytes = declare.Bytes(b"bar")

    foo = Foo()
    assert foo.my_int == 1
    assert foo.my_float == 3.14
    assert foo.my_bool == True
    assert foo.my_str == "Foo"
    assert foo.my_bytes == b"bar"


def test_validate():
    class Foo:
        positive = declare.Int(0)

        @positive.validate
        def _validate_positive(self, value: int) -> int:
            return max(0, value)

    foo = Foo()
    foo.positive = -1
    assert foo.positive == 0
    foo.positive = 1
    assert foo.positive == 1


def test_watch() -> None:
    changes0: list[tuple[int, int]] = []
    changes1: list[tuple[int, int]] = []
    changes2: list[tuple[int, int]] = []
    changes3: list[tuple[int, int]] = []

    class Foo:
        value0 = declare.Int(0)
        value1 = declare.Int(0)

        @value0.watch
        def _watch_value0(self, old: int, new: int) -> None:
            changes0.append((old, new))

        @value0.watch
        def _watch_value1(self, old: int, new: int) -> None:
            changes1.append((old, new))

    foo0 = Foo()
    foo0.value0 = 1
    assert changes0 == [(0, 1)]
    assert changes1 == [(0, 1)]
    foo0.value0 = 2
    assert changes0 == [(0, 1), (1, 2)]
    assert changes1 == [(0, 1), (1, 2)]

    def callback(obj: Foo, old: int, new: int):
        changes3.append((old, new))

    foo1 = Foo()
    watch(foo0, "value1", callback)
    foo0.value1 = 3
    foo1.value1 = 4
    assert changes0 == [(0, 1), (1, 2)]
    assert changes1 == [(0, 1), (1, 2)]
    assert changes3 == [(0, 3)]


def test_custom():
    class Foo:
        things = Declare[List[str]](["foo", "bar"])

    foo = Foo()
    assert foo.things == ["foo", "bar"]

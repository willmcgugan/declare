import declare
from declare import Declare


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
    changes: list[tuple[int, int]] = []

    class Foo:
        value = declare.Int(0)

        @value.watch
        def _watch_foo(self, old: int, new: int) -> None:
            changes.append((old, new))

    foo = Foo()
    foo.value = 1
    assert changes == [(0, 1)]
    foo.value = 2
    assert changes == [(0, 1), (1, 2)]


def test_custom():
    class Foo:
        things = Declare[list[str]](["foo", "bar"])

    foo = Foo()
    assert foo.things == ["foo", "bar"]


def test_on_set():
    values: list[tuple[object, str, int]] = []

    def on_set(obj: object, name: str, val: int) -> None:
        values.append((obj, name, val))

    class Foo:
        value = Declare[int](1, on_set=on_set)

    foo = Foo()
    foo.value = 1
    assert not values
    foo.value = 2
    assert values == [(foo, "value", 2)]

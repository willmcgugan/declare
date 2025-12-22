import declare


def get_numbers() -> list[int]:
    return [1, 1, 2, 3, 5, 8, 13]


def test_list_initialize():
    """Testing various way of initializing."""

    class InitializeTest:
        def get_names(self) -> list[str]:
            return ["foo", "bar", "baz"]

        # The `names` property will call `get_names` to get its default when first referenced.
        names = declare.List(get_names)
        numbers = declare.List(get_numbers)
        foo = declare.List[int]([])
        empty = declare.List(list)

    a = InitializeTest()
    a.foo
    a.empty

    assert a.names == ["foo", "bar", "baz"]
    assert a.numbers == [1, 1, 2, 3, 5, 8, 13]
    assert a.empty == []

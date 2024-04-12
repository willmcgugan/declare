from __future__ import annotations

from copy import copy
from typing import Callable, cast, Generic, overload, Type, TypeVar

from typing_extensions import TypeAlias


ObjectType = TypeVar("ObjectType")
ValueType = TypeVar("ValueType")
Validator: TypeAlias = Callable[[ObjectType, ValueType], ValueType]
Watcher: TypeAlias = Callable[[ObjectType, ValueType | None, ValueType], None]
ValidateMethodType = TypeVar("ValidateMethodType", bound=Validator)
WatchMethodType = TypeVar("WatchMethodType", bound=Watcher)


class NoValue:
    """Sentinel type."""


_NO_VALUE = NoValue()


class DeclareError(Exception):
    """Raised when an Declare related error occurs,"""


class ValidateDecorator(Generic[ValidateMethodType]):
    """Validate decorator.

    Decorate a Widget method to make it a validator for the attribute.
    """

    def __init__(self, declare: Declare | None = None) -> None:
        self._declare = declare
        self._validator: ValidateMethodType | None = None

    @overload
    def __call__(self) -> ValidateDecorator[ValidateMethodType]: ...

    @overload
    def __call__(self, method: ValidateMethodType) -> ValidateMethodType: ...

    def __call__(
        self, method: ValidateMethodType | None = None
    ) -> ValidateMethodType | ValidateDecorator[ValidateMethodType]:
        if method is None:
            return self
        assert self._declare is not None

        if self._declare._validator is not None:
            raise DeclareError(f"A validator has already been set on {self._declare!r}")
        self._declare._validator = method
        return method


class WatchDecorator(Generic[WatchMethodType]):
    """Validate decorator.

    Decorate a Widget method to make it a validator for the attribute.
    """

    def __init__(self, declare: Declare | None = None) -> None:
        self._declare = declare

    @overload
    def __call__(self) -> WatchDecorator[WatchMethodType]: ...

    @overload
    def __call__(self, method: WatchMethodType) -> WatchMethodType: ...

    def __call__(
        self, method: WatchMethodType | None = None
    ) -> WatchMethodType | WatchDecorator[WatchMethodType]:
        if method is None:
            return self
        assert self._declare is not None

        if self._declare._watcher is not None:
            raise DeclareError(f"A watcher has already been set on {self._declare!r}")
        self._declare._watcher = method
        return method


class Declare(Generic[ValueType]):
    """A descriptor to declare attributes."""

    def __init__(
        self,
        default: ValueType,
        *,
        validate: Validator | None = None,
        watch: Watcher | None = None,
    ) -> None:
        self._name = ""
        self._private_name = ""
        self._default = default
        self._validator = validate
        self._watcher = watch
        self._copy_default = not isinstance(default, (int, float, bool, str, complex))

    def copy(self) -> Declare[ValueType]:
        """Return a copy of the Declare descriptor.

        Returns:
            A Declare descriptor.
        """
        declare = Declare(
            self._default,
            validate=self._validator,
            watch=self._watcher,
        )
        return declare

    def __call__(
        self,
        default: ValueType | NoValue = _NO_VALUE,
        *,
        validate: Validator | None = None,
        watch: Watcher | None = None,
    ) -> Declare[ValueType]:
        """Update the declaration.

        Args:
            default: New default.
            validate: A validator function.
            watch: A watch function.

        Returns:
            A new Declare.
        """
        declare = self.copy()
        if not isinstance(default, NoValue):
            declare._default = default
        if validate is not None:
            declare._validator = validate
        if watch is not None:
            declare._watcher = watch
        return declare

    def __set_name__(self, owner: Type, name: str) -> None:
        self._owner = owner
        self._name = name
        self._private_name = f"__declare_private_{name}"

    @overload
    def __get__(
        self: Declare[ValueType], obj: None, obj_type: Type[ObjectType]
    ) -> Declare[ValueType]: ...

    @overload
    def __get__(
        self: Declare[ValueType], obj: ObjectType, obj_type: Type[ObjectType]
    ) -> ValueType: ...

    def __get__(
        self: Declare[ValueType], obj: ObjectType | None, obj_type: Type[ObjectType]
    ) -> Declare[ValueType] | ValueType:
        if obj is None:
            return self
        if isinstance((value := getattr(obj, self._private_name, _NO_VALUE)), NoValue):
            value = copy(self._default) if self._copy_default else self._default
            setattr(obj, self._private_name, value)
            return value
        else:
            return value

    def __set__(self, obj: object, value: ValueType) -> None:
        if self._watcher:
            current_value = getattr(obj, self._name, None)
            new_value = (
                value if self._validator is None else self._validator(obj, value)
            )
            setattr(obj, self._private_name, new_value)
            if current_value != new_value:
                self._watcher(obj, current_value, new_value)

        else:
            setattr(
                obj,
                self._private_name,
                value if self._validator is None else self._validator(obj, value),
            )

    @property
    def optional(self) -> Declare[ValueType | None]:
        """Make the type optional."""
        # We're just changing the type, so this doesn't do anything at runtime.
        return cast("Declare[ValueType | None]", self)

    @property
    def validate(self) -> ValidateDecorator:
        """Decorator to define a validator."""
        return ValidateDecorator(self)

    @property
    def watch(self) -> WatchDecorator:
        """Decorator to create a watcher."""
        return WatchDecorator(self)

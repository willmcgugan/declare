# What?

Declare is a syntactical sugar for adding attributes to Python classes, with support for validation and *watching* attributes for changes.

Declare works well with type-checkers such as MyPy, even though in many cases you don't need to write type annotations.

## Example

let's look at a simple example.
The following code creates a class to represent a color, with attributes for red, green, blue, plus an alpha (transparency) component:

```python
import declare


class Color:
    """A color object with RGB, and alpha components."""

    red = declare.Int(0)
    green = declare.Int(0)
    blue = declare.Int(0)
    alpha = declare.Float(1.0)
```

If you construct a `Color` instance, it will have the four attributes.

Perhaps surprisingly, these attributes are typed -- without any explicit type annotations.
Mypy and other type-checkers will understand that `Color` instances have three `int` attributes, and an additional `float` for alpha.

### Validation

So far, there is little benefit over conventional attributes, but Declare adds a convenient way to add validation.

The following extends the `Color` class with validation for all four attributes:

```python
import declare


class Color:
    """A color object with RGB, and alpha components."""

    red = declare.Int(0)
    green = declare.Int(0)
    blue = declare.Int(0)
    alpha = declare.Float(1.0)

    @red.validate
    @green.validate
    @blue.validate
    def _validate_component(self, component: int) -> int:
        """Restrict RGB to 0 -> 255."""
        return max(0, min(255, component))

    @alpha.validate
    def _validate_alpha(self, alpha: float) -> float:
        return max(0.0, min(1.0, alpha))
```

If you were to attempt to assign a value to an attribute outside of its expected range, that value will be restricted to be within an upper and lower range.
In other words, setting `my_color.red=300` would actually set the `red` attribute to `255`.

You can do anything you wish in the validator to change the value being stored, or perhaps to raise an exception if the value is invalid.

### Watching

In addition to validating attributes, you can *watch* attributes for changes.
When an attribute has a watch method, that method will be called when the value changes.
The method will receive the original value and the new value being set.

Here's the color class extended with a watch method:

```python
import declare


class Color:
    """A color object with RGB, and alpha components."""

    red = declare.Int(0)
    green = declare.Int(0)
    blue = declare.Int(0)
    alpha = declare.Float(1.0)

    @red.validate
    @green.validate
    @blue.validate
    def _validate_component(self, component: int) -> int:
        """Restrict RGB to 0 -> 255."""
        return max(0, min(255, component))

    @alpha.validate
    def _validate_alpha(self, alpha: float) -> float:
        return max(0.0, min(1.0, alpha))

    @alpha.watch
    def _watch_alpha(self, old_alpha: float, alpha: float) -> None:
        print(f"alpha changed from {old_alpha} to {alpha}!")
```

The addition of the `@alpha.watch` decorator will cause the `_watch_alpha` method to be called when any value is assigned to the `alpha` attribute.

### Declare types

In the above code `declare.Int` and `declare.Float` are pre-defined declarations for standard types (there is also `Bool`, `Str`, and `Bytes`).
You can also also declare custom type by importing `Declare`.

let's add a `Palette` class which contains a name, and a list of colors:

```python
import declare
from declare import Declare


class Color:
    """A color object with RGB, and alpha components."""

    red = declare.Int(0)
    green = declare.Int(0)
    blue = declare.Int(0)
    alpha = declare.Float(1.0)

    @red.validate
    @green.validate
    @blue.validate
    def _validate_component(self, component: int) -> int:
        """Restrict RGB to 0 -> 255."""
        return max(0, min(255, component))

    @alpha.validate
    def _validate_alpha(self, alpha: float) -> float:
        return max(0.0, min(1.0, alpha))

    @alpha.watch
    def _watch_alpha(self, old_alpha: float, alpha: float) -> None:
        print(f"alpha changed from {old_alpha} to {alpha}!")


class Palette:
    """A container of colors."""
    name = declare.Str("")
    colors = Declare[list[Color]]([])

```

The `colors` attribute is created with this invocation: `Declare[list[Color]]([])`, which creates a list of colors, defaulting to an empty list.

Let's break that down a bit:

- `Declare` is the descriptor which create the attributes.
- `Declare[list[Color]]` tells the type checker you are declaring a list of Color objects.
- `Declare[list[Color]]([])` sets the default to an empty list. Note that this doesn't suffer from the classic Python issue of default mutable arguments. You will get a new instance every time you construct a `Palette`.


## Installation

Install via `pip` or your favorite package manager.

```bash
pip install declare
```

# Why?

Textual uses a similar approach to declare [reactive attributes](https://textual.textualize.io/guide/reactivity/), which are a useful general programming concept. Alas, without Textual as a runtime, it wouldn't be possible to use Textual's reactive attributes in another project. 

This library extracts some of the core features and makes them work without any other dependencies.

There is some overlap with dataclasses, [Pydantic](https://docs.pydantic.dev/latest/), [attrs](https://www.attrs.org/en/stable/), and other similar projects.
But Declare isn't intended to replace any of these projects, which offer way more features.
In fact, you can add Declared attributes to the class objects created by these other libraries.

# How?

In a word: ["descriptors"](https://mathspp.com/blog/pydonts/describing-descriptors).
Python's descriptor protocol has been around forever, but remains a under used feature, IMHO.

# Who?

- [@willmcgugan](https://twitter.com/willmcgugan)
- [mastodon.social/@willmcgugan](https://mastodon.social/@willmcgugan)


# Thanks!

A huge thank you to [Chris Cardillo](https://github.com/chriscardillo) who very kindly let me have the `declare` name on Pypi.

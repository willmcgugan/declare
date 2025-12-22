import declare


class Color:
    """A color object with RGB, and alpha components."""

    red = declare.Int(0)
    green = declare.Int(0)
    blue = declare.Int(0)
    alpha = declare.Float(1.0)

    @declare.init
    def __init__(self, red: int, green: int, blue: int, *, alpha: float = 1.0): ...

    @red.validate
    @green.validate
    @blue.validate
    def validate_component(self, component: int) -> int:
        """Restrict RGB to 0 -> 255."""
        return max(0, min(255, component))

    @alpha.validate
    def validate_alpha(self, alpha: float) -> float:
        return max(0.0, min(1.0, alpha))

    @alpha.watch
    def watch_alpha(self, old_alpha: float, alpha: float) -> None:
        print(f"alpha changed from {old_alpha} to {alpha}!")


class Palette:
    """A palette"""

    name = declare.Str("")
    colors = declare.Dict[str, Color]({})


if __name__ == "__main__":
    red = Color(0, 0, 0)
    red.red = 300
    red.alpha = 0.5
    print(red.red, red.green, red.blue)

    palette = Palette()
    palette.colors = {"red": Color(255, 0, 0)}

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
    name = declare.Str("")
    colors = Declare[list[Color]]([])


if __name__ == "__main__":
    red = Color()
    red.red = 300
    red.alpha = 0.5
    print(red.red, red.green, red.blue)

    palette = Palette()
    palette.colors = [Color()]

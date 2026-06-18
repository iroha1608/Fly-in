"""ColorManager module for managing colors in the terminal."""
import re


class ColorManager:
    """ColorManager class for managing colors in the terminal.

    This class provides methods to convert color names and hex values to ANSI
    escape codes for terminal output. It also includes a predefined set of
    colors and a rainbow color sequence for visual effects.

    Attributes:
        COLORS (dict): A dictionary mapping color names to their hex values.
        RAINBOW (list):
            A list of hex values representing a rainbow color sequence.
        RESET (str): The ANSI escape code to reset terminal colors.
        DEFAULT (str): The default hex color value.

    """
    COLORS = {
        "red": "#FF3C3C",
        "green": "#32DC64",
        "yellow": "#FFD200",
        "blue": "#2878FF",
        "magenta": "#EB3CEB",
        "cyan": "#28D2E6",
        "gray": "#828282",
        "orange": "#FF8C00",
        "purple": "#8C28E6",
        "brown": "#964B00",
        "lime": "#78FF00",
        "maroon": "#800000",
        "darkred": "#8B0000",
        "crimson": "#DC143C",
        "pink": "#FF69B4",
        "violet": "#EE82EE",
        "gold": "#FFD700",

        "black": "#444444",
        "white": "#FFFFFF"
    }
    RAINBOW = [
        COLORS["red"],
        COLORS["orange"],
        COLORS["yellow"],
        COLORS["green"],
        COLORS["cyan"],
        COLORS["blue"],
        COLORS["purple"]
    ]
    RESET = "\33[0m"
    DEFAULT = "#FFFFFF"

    @classmethod
    def get_hex(cls, color_name: str | None) -> str:
        """Returns the hex value for a given color name or hex string.

        If the input is a valid hex string (e.g., "#RRGGBB"), it returns the
        uppercase version of that string. If the input is a recognized
        color name, it returns the corresponding hex value. If the input is
        None or not recognized, it returns the default hex value.

        Args:
            color_name (str | None): The color name or hex string to convert.

        Returns:
            str: The corresponding hex value or the default hex value.

        """
        if not color_name:
            return cls.DEFAULT

        color_input = color_name.strip()

        if color_input.startswith("#") and len(color_name) == 7:
            if re.match(r"^#[0-9a-fA-F]{6}$", color_input):
                return color_input.upper()

        return cls.COLORS.get(color_input.lower(), cls.DEFAULT)

    @classmethod
    def hex_to_ansi(cls, color_name: str) -> str:
        """Converts a hex color string to an ANSI escape code.

        Args:
            color_name (str): The hex color string (e.g., "#RRGGBB").

        Returns:
            str: The corresponding ANSI escape code.

        """
        hex_color = color_name.lstrip("#")
        if len(hex_color) != 6:
            return ""

        try:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            return f"\33[38;2;{r};{g};{b}m"
        except ValueError:
            return ""

        return ""

    @classmethod
    def get_ansi(cls, color_name: str | None) -> str:
        """Returns the ANSI escape code for a given color name or hex string.

        Args:
            color_name (str | None): The color name or hex string to convert.

        Returns:
            str: The corresponding ANSI escape code or an empty string if the
            input is None or invalid.

        """
        if not color_name:
            return ""

        hex_val = cls.get_hex(color_name)
        return cls.hex_to_ansi(hex_val)

    @classmethod
    def get_ansi_reset(cls) -> str:
        """Returns the ANSI escape code to reset terminal colors.

        Returns:
            str: The ANSI escape code to reset terminal colors.

        """
        return cls.RESET

    @classmethod
    def get_ansi_rainbow(cls, text: str) -> str:
        """Returns the input text with a rainbow color effect applied.

        Args:
            text (str): The input text to colorize.

        Returns:
            str: The input text with a rainbow color effect applied.

        """
        result: str = ""
        for i, char in enumerate(text):
            result += cls.hex_to_ansi(cls.RAINBOW[i % len(cls.RAINBOW)]) + char
        return result

class ColorManager:
    """
        TerminalVisualizer, GUIVisualizerの色を管理する。
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
    def get_hex(cls, color_name: str) -> str:
        """
            色名、RGBから表記の検証。
            # から始まるときはそのまま返し、
            文字列の時は辞書から探す。
        """
        if not color_name:
            return cls.DEFAULT

        color_input = color_name.strip()

        if color_input.startswith("#") and len(color_name) ==  7:
            if re.match(r"^#[0-9a-fA-F]{6}$", color_input):
                return color_input.upper()

        return cls.COLORS.get(color_input.lower(), cls.DEFAULT)

    @classmethod
    def hex_to_ansi(cls, color_name: str) -> str:
        """RGBの文字列をANSIに変換する。 """
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
    def get_ansi(cls, color_name: str) -> str:
        """色名からTerminal用のANSIを取得する。"""
        if not color_name:
            return ""

        hex_val = cls.get_hex(color_name)
        return cls.hex_to_ansi(hex_val)

    @classmethod
    def get_ansi_reset(cls) -> str:
        """TerminalのANSIをRESETする文字列を返す。"""
        return cls.RESET

    @classmethod
    def get_ansi_rainbow(cls, text) -> str:
        """textをANSIでRainbowにし文字列を返す。"""
        result: str = ""
        for i, char in enumerate(text):
            result += cls.hex_to_ansi(cls.RAINBOW[i % len(cls.RAINBOW)]) + char
        return result

from Graph import Graph


class TerminalVisualizer:
    COLORS = {
        "red": (255, 60, 60),
        "green": (50, 210, 90),
        "yellow": (255, 210, 0),
        "blue": (40, 120, 255),
        "magenta": (235, 60, 235),
        "cyan": (40, 210, 230),
        "gray": (130, 130, 130),
        "orange": (255, 140, 0),
        "purple": (140, 40, 230),
        "brown": (150, 75, 0),
        "lime": (120, 255, 0),
        "maroon": (128, 0, 0),
        "darkred": (139, 0, 0),
        "crimson": (220, 20, 60),
        "pink": (255, 105, 180),
        "lightgray": (200, 200, 200),
        "darkblue": (0, 0, 139),
        "teal": (0, 128, 128),
        "navy": (0, 0, 128),
        "olive": (128, 128, 0),
        "gold": (255, 215, 0),
        "white": (255, 255, 255)
    }
    RESET = "\33[0m"

    def __init__(self, graph: Graph) -> None:
        self.graph = graph

    def get_rgb_sequence(self, color_str: str) -> str:
        """
            色、カラーコードからANSI RGBエスケープシークエンスを返す。
        """
        if not color_str:
            return ""

        color_str = color_str.lower().strip()
        if color_str in self.COLORS:
            r, g, b = self.COLORS[color_str]
            return f"\33[38;2;{r};{g};{b}m"

        if color_str.startswith("#") and len(color_str) ==  7:
            try:
                r = int(color_str[1:3], 16)
                g = int(color_str[3:5], 16)
                b = int(color_str[5:7], 16)
                return f"\33[38;2;{r};{g};{b}m"
            except ValueError:
                return ""

        return ""

    def colorize(self, zone_name: str) -> str:
        if zone_name in self.graph.zones:
            color_str = self.graph.zones[zone_name].color
            color_sequence = self.get_rgb_sequence(color_str)
            if color_sequence:
                return f"{color_sequence}{zone_name}{self.RESET}"
        return zone_name

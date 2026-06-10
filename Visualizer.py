COLORS = {
    "red": (255, 60, 60),
    "green": (50, 220, 100),
    "yellow": (60, 130, 255),
    "blue": (250, 210, 20),
    "magenta": (230, 50, 230),
    "cyan": (30, 200, 220),
    "gray": (120, 120, 120),
    "orange": (255, 165, 0),
    "purple": (128, 0, 128),
    "brown": (165, 42, 42),
    "lime": (50, 205, 50),
    "maroon": (102, 43, 44),
    "darkred": (139, 0, 0),
    "crimson": (220, 20, 60),
    "white": (255, 255, 255)
}
RESET = "\33[0m"


def get_rgb_sequence(color_str: str) -> str:
    """
        色、カラーコードからANSI RGBエスケープシークエンスを返す。
    """
    if not color_str:
        return ""
    color_str = color_str.lower().strip()
    if color_str in COLORS:
        r, g, b = COLORS[color_str]
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

def colorize(zone_name: str, graph) -> str:
    if zone_name in graph.zones:
        color_str = graph.zones[zone_name].color
        color_sequence = get_rgb_sequence(color_str)
        if color_sequence:
            return f"{color_sequence}{zone_name}{RESET}"
    return zone_name

from Graph import Graph
from ColorManager import ColorManager


class TerminalVisualizer:

    def __init__(self, graph: Graph) -> None:
        self.graph = graph

    def colorize(self, zone_name: str) -> str:
        if zone_name in self.graph.zones:
            # Zoneのcolorを取得
            color_name = self.graph.zones[zone_name].color

            # 色名、RGBからANSIに変換
            ansi_color = ColorManager.get_ansi(color_name)
            reset_color = ColorManager.get_ansi_reset()

            if ansi_color and reset_color:
                return f"{ansi_color}{zone_name}{reset_color}"

        return zone_name

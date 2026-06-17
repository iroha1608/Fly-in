from Graph import Graph
from Drone import Drone
from ColorManager import ColorManager


class TerminalVisualizer:
    """
        Terminalに描画するためのクラス。
    """

    def __init__(self, graph: Graph, drones: list[Drone]) -> None:
        self.graph = graph
        self.drones = drones
        self.max_turns = (
            max(len(d.planned_path) for d in drones) if drones else 0
        )

    def _colorize(self, zone_name: str) -> str:
        """色名、RGBからANSIに変換"""
        if zone_name in self.graph.zones:
            # Zoneのcolorを取得
            color_name = self.graph.zones[zone_name].color
            reset_color = ColorManager.get_ansi_reset()

            if color_name == "rainbow":
                result_color = ColorManager.get_ansi_rainbow(zone_name)
                if result_color and reset_color:
                    return f"{result_color}{reset_color}"
            else:
                ansi_color = ColorManager.get_ansi(color_name)
                if ansi_color and reset_color:
                    return f"{ansi_color}{zone_name}{reset_color}"

        return zone_name

    def get_info(self, current_location: str, turn: int) -> tuple[int, float | int]:
            name1, name2 = current_location.split("-")
            zone1 = self.graph.zones[name1]
            for connection in zone1.connections:
                if connection.target_zone.name == name2:
                    return connection.get_info(turn)

    def start(self, capacity_info: bool = False) -> None:
        """
            Terminalへの描画開始。
        """
        for turn in range(1, self.max_turns + 1):
            turn_output = []
            capacity_output = []
            seen_location = {}

            for drone in self.drones:
                if drone.has_moved(turn):
                    current_location = drone.get_location(turn)

                    if "-" in current_location:
                        parts = current_location.split("-")
                        colored_parts = [self._colorize(p) for p in parts]
                        colored_location = "-".join(colored_parts)

                        current_cap, max_cap = self.get_info(current_location, turn)
                        capacity_output.append(f"{colored_location}: ({current_cap} / {max_cap}) drones")

                    else:
                        colored_location = self._colorize(current_location)
                        current_cap, max_cap = self.graph.zones[current_location].get_info(turn)
                        capacity_output.append(f"{colored_location}: ({current_cap} / {max_cap}) drones")

                    turn_output.append(f"{drone.id}-{colored_location}")

            if turn_output:
                print("Turn: " + " ".join(turn_output))
            if capacity_info:
                print("        " + " ".join(capacity_output), end="")
                print(" capacity used")

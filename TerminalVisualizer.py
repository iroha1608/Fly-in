"""Terminal Visualizer class for the Fly-in System.

This class is responsible for visualizing the simulation in the terminal.

"""
from Graph import Graph
from Drone import Drone
from ColorManager import ColorManager


class TerminalVisualizer:
    """Terminal Visualizer class for the Fly-in System.

    This class is responsible for visualizing the simulation in the terminal.

    Attributes:
        graph (Graph): The graph representing the zones and connections.
        drones (list[Drone]):
            A list of Drone objects participating in the simulation.
        max_turns (int): The maximum number of turns in the simulation.

    """

    def __init__(self, graph: Graph, drones: list[Drone]) -> None:
        """Initializes the TerminalVisualizer with the given graph and drones.

        Args:
            graph (Graph): The graph representing the zones and connections.
            drones (list[Drone]):
                A list of Drone objects participating in the simulation.

        """
        self.graph = graph
        self.drones = drones
        self.max_turns = (
            max(len(d.planned_path) for d in drones) if drones else 0
        )

    def _colorize(self, zone_name: str) -> str:
        """Returns the colorized string for the given zone name.

        Args:
            zone_name (str): The name of the zone to colorize.

        Returns:
            str: The colorized string for the given zone name.

        """
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

    def start(self) -> None:
        """Starts the terminal visualization of the simulation."""
        for turn in range(1, self.max_turns + 1):
            turn_output: list[str] = []

            for drone in self.drones:
                if drone.has_moved(turn):
                    current_location = drone.get_location(turn)

                    if "-" in current_location:
                        parts = current_location.split("-")
                        colored_parts = [self._colorize(p) for p in parts]
                        colored_location = "-".join(colored_parts)

                    else:
                        colored_location = self._colorize(current_location)

                    turn_output.append(f"{drone.id}-{colored_location}")

            if turn_output:
                print(" ".join(turn_output))

from TerminalVisualizer import TerminalVisualizer
from GUIVisualizer import GUIVisualizer
from Graph import Graph
from Drone import Drone


class SimulationEngine:
    """
    """
    def __init__(self, graph: Graph, drones: list[Drone]) -> None:
        self.graph = graph
        self.drones = drones
        self.visualizer = TerminalVisualizer(graph)

    def run_simulation(self) -> None:
        # すべてのドローンの中から、一番多いターン数を取得。
        max_turns = max(len(d.planned_path) for d in self.drones) if self.drones else 0

        for turn in range(1, max_turns + 1):
            turn_output = []

            for drone in self.drones:
                if drone.has_moved(turn):
                    current_location = drone.get_location(turn)

                    if "-" in current_location:
                        parts = current_location.split("-")
                        colored_parts = [self.visualizer.colorize(p) for p in parts]
                        colored_location = "-".join(colored_parts)

                    else:
                        colored_location = self.visualizer.colorize(current_location)

                    turn_output.append(f"{drone.id}-{colored_location}")

            if turn_output:
                print(f"Turn{turn}: " + " ".join(turn_output))

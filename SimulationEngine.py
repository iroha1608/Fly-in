from Graph import Graph
from Drone import Drone
from PathFinder import PathFinder
from TerminalVisualizer import TerminalVisualizer
from GUIVisualizer import GUIVisualizer

INFO = "[\33[32mINFO\33[0m]: "
WARNING = "[\33[33mWARNING\33[0m]: "


class SimulationEngine:
    """
        Terminal, GUIへの描写をシミュレーションするクラス。
    """
    def __init__(self, graph: Graph) -> None:
        self.graph = graph
        self.drones: list[Drone] = []

    def find_path(self) -> None:
        """
            Graphから最短経路を取得する。
        """
        pathfinder = PathFinder(self.graph)

        for i in range(1, self.graph.nb_drones + 1):
            drone_id = f"D{i}"
            drone = Drone(drone_id, self.graph.start_zone.name)

            # SearchStateのpath_historyを取得
            path = pathfinder.find_path_for_single_drone(start_turn=0)
            if not path:
                raise ValueError(
                    f"Drone ID: {drone_id} No Path found to the goal."
                ) from e

            pathfinder.commit_path(path)
            drone.set_path(path)
            self.drones.append(drone)

    def run_simulation(self) -> None:
        """
            Terminal, GUIへの描画を開始。
        """
        # Terminalの描画
        print(f"{INFO}Starting Terminal Visualizer...")
        cli = TerminalVisualizer(self.graph, self.drones)
        cli.start()

        # GUIの描画
        print(f"{INFO}Starting GUI Visualizer...")
        gui = GUIVisualizer(self.graph, self.drones)
        gui.start()

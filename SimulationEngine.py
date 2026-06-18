"""SimulationEngine module for the Fly-in System.

This module contains the SimulationEngine class, which is responsible for
managing the simulation of drones navigating through a graph. It handles
the pathfinding for each drone and visualizes the simulation in both
terminal and GUI formats.

"""
from Graph import Graph
from Drone import Drone
from PathFinder import PathFinder
from TerminalVisualizer import TerminalVisualizer
from GUIVisualizer import GUIVisualizer

INFO = "[\33[32mINFO\33[0m]: "
WARNING = "[\33[33mWARNING\33[0m]: "


class SimulationEngine:
    """SimulationEngine class for the Fly-in System.

    This class is responsible for managing the simulation of drones navigating
    through a graph. It handles the pathfinding for each drone and visualizes
    the simulation in both terminal and GUI formats.

    Attributes:
        graph (Graph): The graph representing the zones and connections.
        drones (list[Drone]):
            A list of Drone objects participating in the simulation.

    """
    def __init__(self, graph: Graph) -> None:
        """Initializes the SimulationEngine with the given graph.

        Args:
            graph (Graph): The graph representing the zones and connections.

        """
        self.graph = graph
        self.drones: list[Drone] = []

    def find_path(self) -> None:
        """Finds paths for all drones in the simulation."""
        pathfinder = PathFinder(self.graph)

        for i in range(1, self.graph.nb_drones + 1):
            drone_id = f"D{i}"
            drone = Drone(drone_id, self.graph.start_zone.name)

            # SearchStateのpath_historyを取得
            path = pathfinder.find_path_for_single_drone(start_turn=0)
            if not path:
                raise ValueError(
                    f"Drone ID: {drone_id} No Path found to the goal."
                )

            pathfinder.commit_path(path)
            drone.set_path(path)
            self.drones.append(drone)

    def run_simulation(self) -> None:
        """Runs simulation and visualizes the output in terminal and GUI."""
        # Terminalの描画
        print(f"{INFO}Starting Terminal Visualizer...")
        cli = TerminalVisualizer(self.graph, self.drones)
        cli.start()

        # GUIの描画
        print(f"{INFO}Starting GUI Visualizer...")
        gui = GUIVisualizer(self.graph, self.drones)
        gui.start()

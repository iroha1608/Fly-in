import sys
import time

from Parser import Parser, CLIConfig , parse_arguments
from PathFinder import PathFinder
from Drone import Drone
from SimulationEngine import SimulationEngine
from GUIVisualizer import GUIVisualizer


INFO = "[\33[32mINFO\33[0m]: "
ERROR = "[\33[31mERROR\33[0m]: "
WARNING = "[\33[33mWARNING\33[0m]: "
TIME = 0.2

def main() -> None:
    print("-------------------- Fly-in System Started --------------------")
    time.sleep(TIME)
    parser = Parser()
    print(f"{INFO}Parser has been loaded!")
    time.sleep(TIME)
    config: CLIConfig = parse_arguments()

    try:
        graph = parser.parse_file(config.map)
    except ValueError as e:
        print(f"{ERROR}Parsing error: {e}", file=sys.stderr)
        sys.exit(1)
    print(f"{INFO}Map data has been loaded!")
    # TODO: Parseする時にゴミ文字とか入ってたらWARNING使う。
    time.sleep(TIME)

    print(f"        Drones: {graph.nb_drones}")
    time.sleep(TIME)
    print(f"        Start: '{graph.start_zone.name}'"
          f" -> Goal: '{graph.end_zone.name}'")
    time.sleep(TIME)

    drones: list[Drone] = []
    pathfinder = PathFinder(graph)

    for i in range(1, graph.nb_drones + 1):
        drone_id = f"D{i}"
        drone = Drone(drone_id, graph.start_zone.name)

        # SearchStateのpath_historyを取得
        path = pathfinder.find_path_for_single_drone(start_turn=0)
        if not path:
            print(f"{ERROR}Drone ID: {drone_id} No Path found to the goal.")
            sys.exit(1)

        pathfinder.commit_path(path)
        drone.set_path(path)
        drones.append(drone)

    print(f"{INFO}Path Found!")
    time.sleep(TIME)

    print("-------------------- Simulation Output --------------------")
    time.sleep(TIME)

    engine = SimulationEngine(graph, drones)
    engine.run_simulation()

    print(f"{INFO}Starting GUI Visualizer...")
    gui = GUIVisualizer(graph, drones)
    gui.start()


if __name__ == "__main__":
    main()

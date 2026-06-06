import sys
import time

from Parser import Parser, CLIConfig , parse_arguments
from PathFinder import PathFinder


INFO = "[\33[32mINFO\33[0m]: "
ERROR = "[\33[31mERROR\33[0m]: "
WARNING = "[\33[33mWARNING\33[0m]: "
TIME = 0.2

def main() -> None:
    print("--------------- Fly-in System Started ---------------")
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
    time.sleep(TIME)

    print(f"Drones: {graph.nb_drones}")
    time.sleep(TIME)
    print(f"Start: {graph.start_zone.name} -> Goal: {graph.end_zone.name}")
    time.sleep(TIME)

    pathfinder = PathFinder(graph)
    print("Running single drone pathfinding...")
    path = pathfinder.find_path_for_single_drone(start_turn=0)

    if path:
        print("-------------------- Path Found! --------------------")
        time.sleep(TIME)
        for turn, location in enumerate(path, start=1):
            print(f"Turn {turn}: D1-{location}")
            time.sleep(TIME)
    else:
        print(f"{ERROR}No Path found to the goal.")


if __name__ == "__main__":
    main()

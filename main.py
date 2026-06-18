"""Fly-in System main program.

This program is the entry point for the Fly-in System.
Initializes the system, parses the map file, and starts the simulation engine.

"""
import sys
import time

from Parser import Parser
from SimulationEngine import SimulationEngine

INFO = "[\33[32mINFO\33[0m]: "
ERROR = "[\33[31mERROR\33[0m]: "
WARNING = "[\33[33mWARNING\33[0m]: "
TIME = 0.2


def main() -> None:
    """

    Main function to start the Fly-in System.
    Initializes the parser, loads the map data, starts the simulation engine,
    finds the shortest path, and runs the simulation with visual output.

    """
    print("-------------------- Fly-in System Started ---------------------")

    # ------------------------ Map fileのパース処理 -------------------------
    parser = Parser()
    print(f"{INFO}Parser has been loaded!")
    time.sleep(TIME)
    try:
        config = parser.parse_arguments()
        graph = parser.parse_file(config.map)
    except ValueError as e:
        print(f"{ERROR}Parsing error: {e}", file=sys.stderr)
        sys.exit(1)
    print(f"{INFO}Map data has been loaded!")
    time.sleep(TIME)
    print(f"        Drones: {graph.nb_drones}")
    time.sleep(TIME)
    print(f"        Start: '{graph.start_zone.name}'"
          f" -> Goal: '{graph.end_zone.name}'")
    time.sleep(TIME)

    # ----------------------- Simulation Engineの起動 -----------------------
    engine = SimulationEngine(graph)
    print(f"{INFO}Simulation engine has been loaded!")
    time.sleep(TIME)

    # -------------------------- 最短経路探索処理 ---------------------------
    try:
        engine.find_path()
    except ValueError as e:
        print(f"{ERROR}PathFinder error: {e}", file=sys.stderr)
        sys.exit(1)
    print(f"{INFO}Path Found!")
    time.sleep(TIME)

    # --------------------------- Visualizerの起動 --------------------------
    print("---------------------- Simulation Output -----------------------")
    engine.run_simulation()
    print("-------------------- Fly-in System Finished --------------------")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"{WARNING}Program stopped.")
        sys.exit(1)

import sys
import time

from Parser import Parser, CLIConfig , parse_arguments
from PathFinder import PathFinder


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

    pathfinder = PathFinder(graph)
    all_paths: dict[str, list[str]] = {}

    for i in range(1, graph.nb_drones + 1):
        # SearchStateのpath_historyを取得
        drone_id = f"D{i}"
        path = pathfinder.find_path_for_single_drone(start_turn=0)

        if not path:
            print(f"{ERROR}Drone ID: {drone_id} No Path found to the goal.")
            sys.exit(1)
        pathfinder.commit_path(path)
        all_paths[drone_id] = path

    print(f"{INFO}Path Found!")
    time.sleep(TIME)

    print("-------------------- Simulation Output --------------------")
    time.sleep(TIME)

    # すべてのドローンの中から、一番多いターン数を取得。
    max_turns = max(len(p) for p in all_paths.values()) if all_paths else 0

    for turn in range(1, max_turns + 1):
        turn_output = []

        for d_id, path in all_paths.items():
            if turn <= len(path):
                current_location = path[turn - 1]
                previous_location = path[turn - 2] if turn > 1 else graph.start_zone.name

                # ドローンが動いている場合、出力を追加。
                if current_location != previous_location:
                    turn_output.append(f"{d_id}-{current_location}")

        if turn_output:
            print(f"Turn{turn}: ", end="")
            print(" ".join(turn_output))

    time.sleep(TIME)


if __name__ == "__main__":
    main()

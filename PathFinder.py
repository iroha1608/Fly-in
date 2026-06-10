import heapq
import math

from Graph import Graph
from SearchState import SearchState


class PathFinder:
    """
    """
    def __init__(self, graph: Graph) -> None:
        self.graph = graph

    def find_path_for_single_drone(self, start_turn: int = 0) -> list[str]:
        """
            1機のドローンに対するダイクストラ法を用いた経路探索
            Returns:
                各ターンでのZone, Connectionのリスト
        """
        queue: list[SearchState] = []
        heapq.heappush(queue, SearchState(
            cost=0,
            turn=start_turn,
            current_zone=self.graph.start_zone,
            path_history=[]
        ))

        visited: dict[tuple[int, str], int] = {}

        while queue:
            state = heapq.heappop(queue)

            # ゴール判定
            if state.current_zone == self.graph.end_zone:
                return state.path_history

            # 訪問済みチェック
            # より低コストで同じ時間に同じ場所に到達してるならスキップ
            state_key = (state.turn, state.current_zone.name)
            if visited.get(state_key, math.inf) <= state.cost:
                continue
            visited[state_key] = state.cost

            next_turn = state.turn + 1

            # その場で待機判定
            if state.current_zone.can_enter(next_turn):
                heapq.heappush(queue, SearchState(
                    cost=state.cost + 1,
                    turn=next_turn,
                    current_zone=state.current_zone,
                    path_history=state.path_history + [state.current_zone.name]
                ))

            # 隣接Zoneへの移動
            for connection in state.current_zone.connections:
                target = connection.target_zone
                connection_name = f"{state.current_zone.name}-{target.name}"

                # "type=blocked": 侵入不可
                if target.zone_type == "blocked":
                    continue

                # "type=restricted": 2ターン消費かつ2ターン後の予約チェック
                elif target.zone_type == "restricted":
                    if connection.can_enter(next_turn) and target.can_enter(state.turn + 2):
                        heapq.heappush(queue, SearchState(
                            cost=state.cost + 2,
                            turn=state.turn + 2,
                            current_zone=target,
                            path_history=state.path_history + [connection_name, target.name]
                        ))
                # "type=normal, priority": 1ターン消費
                else:
                    if connection.can_enter(next_turn) and target.can_enter(next_turn):
                        heapq.heappush(queue, SearchState(
                            cost=state.cost + 1,
                            turn=state.turn + 1,
                            current_zone=target,
                            path_history=state.path_history + [target.name]
                        ))

        # ゴールに到達しなかった場合
        return []

    def commit_path(self, path_history: list[str]) -> None:
        """
            SearchStateから確定したpathを取り出し、
            各Zone, Connectionに予約する。
        """
        # 初期位置: start_zone
        current_location_name = self.graph.start_zone.name

        for i, location_name in enumerate(path_history):
            turn = i + 1

            # Connection上の移動時
            if "-" in location_name:
                # restricted: start-normal_hub
                name1, name2 = location_name.split("-")
                # Zoneの持っているConnectionを1つづつチェック
                for connection in self.graph.zones[name1].connections:
                    if connection.target_zone.name == name2:
                        connection.reserve(turn)
                        break
                current_location_name = location_name

            # Zoneへの移動、または待機時
            else:
                self.graph.zones[location_name].reserve(turn)
                # 移動時かつ前のターンがConnection上ではない時
                if current_location_name != location_name and "-" not in current_location_name:
                    # Connectionを走査し、移動したZoneがあれば予約する。
                    for connection in self.graph.zones[current_location_name].connections:
                        if connection.target_zone.name == location_name:
                            connection.reserve(turn)
                            break
                current_location_name = location_name

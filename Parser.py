"""コマンドライン引数をパースし、バリデーションのチェックをする。"""
import re
import sys
import math
import argparse
from pathlib import Path
from collections import deque
from typing import Any
from pydantic import BaseModel, Field, ValidationError

from Zone import Zone
from Graph import Graph

WARNING = "[\33[33mWARNING\33[0m]: "


class CLIConfig(BaseModel):
    """コマンドライン引数の情報"""
    map: Path = Field(
        default=Path("maps/original/test_map.txt"),
        description="Path to the map file"
    )


class ParserError(ValueError):
    """パース中に発生したエラーを行番号とともに保持するカスタムエラー"""
    pass


class Parser:
    """"""
    def __init__(self) -> None:
        self.seen_connections: set[str | Any] = set()
        self.VALID_ZONE_KEYS = {"zone",  "color", "max_drones"}
        self.VALID_ZONE_TYPE = {"normal", "blocked", "restricted", "priority"}
        self.VALID_CONNECTIONS_KEYS = {"max_link_capacity"}

    @staticmethod
    def parse_arguments() -> CLIConfig:
        """コマンドライン引数をパースし、CLIConfigで検証し返す。"""
        parser = argparse.ArgumentParser(
            description="Fly-in Drones Simulation")
        parser.add_argument(
            "-m", "--map",
            type=str,
            help="Path to the map file"
        )
        # action="store_true" で引数が不要になる

        try:
            # 解析、不正な引数は自動でSystemExitが呼ばれhelpが出る
            args = parser.parse_args()
            kwargs = {k: v for k, v in vars(args).items() if v is not None}
            # pydanticによる型検証、安全なデータモデルの生成
            return CLIConfig(**kwargs)

        except ValidationError as e:
            raise ValueError("Argument validation failed.") from e

        except Exception as e:
            raise ValueError(f"Unexpected error during parsing. {e}")

    @staticmethod
    def _parse_metadata(metadata_str: str) -> dict[str, str]:
        """"""
        metadata: dict[str, str] = {}
        if not metadata_str:
            return metadata

        content_match = re.search(r'\[(.*?)\]', metadata_str)
        if content_match:
            pairs = content_match.group(1).split()
            for pair in pairs:
                if "=" in pair:
                    key, value = pair.split('=', 1)
                    metadata[key] = value
                else:
                    raise ValueError(
                        f"Invalid metadata format \"{pair}\". "
                        "Expected key=value.")

        return metadata

    @staticmethod
    def _prune_dead_end(graph: Graph) -> None:
        """
            行き止まりのノードを探索時に含めないように、
            is_pruned = Trueにする。
        """
        while True:
            removed_any = False
            for zone in graph.zones.values():
                # 枝刈り済み、スタート、ゴールはスキップ。
                if (zone.is_pruned
                        or zone == graph.start_zone
                        or zone == graph.end_zone):
                    continue

                # まだ枝刈りされていない接続先を調べる。
                active_connections = [
                    con
                    for con in zone.connections
                    if not con.target_zone.is_pruned
                ]

                # 接続先が来る道しか無い(行き止まり)道は枝切り。
                if len(active_connections) <= 1:
                    zone.is_pruned = True
                    removed_any = True

            # 枝切りが終わったらループ終了。
            if not removed_any:
                break

    @staticmethod
    def _validate_connectivity(graph: Graph) -> None:
        """GraphからStart -> Endまで到達可能なマップかチェック"""
        if not graph.start_zone or not graph.end_zone:
            raise ParserError(
                "Map validation failed: Missing start_hub or end_hub")

        queue = deque([graph.start_zone])
        visited = {graph.start_zone.name}

        while queue:
            current = queue.popleft()
            if current == graph.end_zone:
                return
            for connection in current.connections:
                target = connection.target_zone
                if (target.name not in visited
                        and target.zone_type != "blocked"
                        and not target.is_pruned):
                    visited.add(target.name)
                    queue.append(target)
        raise ParserError(
            "Map validation failed: "
            "No valid path exists from start_hub to end_hub."
        )

    def parse_file(self, filepath: Path) -> Graph:
        """
        """
        pattern_drones = re.compile(r"^nb_drones:\s*(-?\d+)$")
        pattern_zone = re.compile(
            r"^(start_hub|end_hub|hub):"
            r"\s+([^\s\-]+)\s+(-?\d+)\s+(-?\d+)(?:\s+\[(.*?)\](.*))?$")
        pattern_connection = re.compile(
                r"^connection:\s+([^\s\-]+)-([^\s\-]+)(?:\s+\[(.*?)\](.*))?$")

        nb_drones = 0
        start_zone = None
        end_zone = None
        zones: dict[str, Zone] = {}
        connections_data = []
        seen_coordinates = set()

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                is_first_valid_line = True

                for i, line in enumerate(f, 1):
                    # コメント行を飛ばす。
                    line = line.split("#")[0].strip()
                    if not line:
                        continue

                    # -------------------- nb_dronesの処理 ------------------
                    # コマンドと空行を無視した最初の行は必ず"nb_drones"
                    if is_first_valid_line:
                        # "nb_drones"パターン以外を弾く
                        match = pattern_drones.match(line)
                        if not match:
                            raise ParserError(
                                f"Line {i}: "
                                "The first valid line must be \"nb_drones\".")

                        # dronesの数が1以上の整数でなければ弾く
                        try:
                            drones = int(match.group(1))
                            if drones <= 0:
                                raise ValueError
                        except ValueError:
                            raise ParserError(
                                f"Line {i}: "
                                "\"nb_drones\" must be greater than 0.")

                        # graphにdronesの数を追加
                        nb_drones = drones
                        is_first_valid_line = False
                        continue

                    # "nb_drones"が再度読み込まれた場合弾く
                    if line.startswith("nb_drones:"):
                        raise ParserError(
                            f"Line {i}: \"nb_drones\" "
                            "must be defined once at the first line.")

                    # ----------------------- hubの処理 ---------------------
                    if line.startswith(("start_hub:", "end_hub:", "hub:")):
                        # "hub"パターン以外を弾く
                        match = pattern_zone.match(line)
                        if not match:
                            raise ParserError(
                                f"Line {i}: Invalid zone definition format.")

                        # Zoneの種別、名前、座標、メタデータを取得
                        z_prefix, name, x_str, y_str, meta_str, garbage = (
                            match.groups())
                        if garbage and garbage.strip():
                            print(
                                f"{WARNING}Line {i}: "
                                "Ignored trailing characters "
                                f"\"{garbage.strip()}\" "
                                "after metadata.", file=sys.stderr)
                        try:
                            x, y = int(x_str), int(y_str)
                        except ValueError:
                            raise ParserError(
                                f"Line {i}: Zone \"{name}\" "
                                f"{x}, {y} must be a positive integer.")

                        # メタデータ内にゴミ文字があったら弾く
                        try:
                            meta = self._parse_metadata(
                                    f"[{meta_str}]" if meta_str else "")
                        except ValueError as e:
                            raise ParserError(f"Line {i}: {e}")

                        # hubのメタデータ以外弾く
                        for key in meta.keys():
                            if key not in self.VALID_ZONE_KEYS:
                                raise ParserError(
                                    f"Unkown metadata key \"{key}\" "
                                    "for a zone. Allowed keys are "
                                    f"{self.VALID_ZONE_KEYS}")

                        # Zoneの座標が同じものを弾く
                        coord_key = (x, y)
                        if coord_key in seen_coordinates:
                            raise ParserError(
                                f"Line {i}: Zone \"{name}\" "
                                "has overlapping coordinates."
                                f"{x}, {y} with another zone.")
                        seen_coordinates.add(coord_key)

                        # zoneの処理
                        z_type = meta.get("zone", "normal")
                        # 許可されたtype以外を弾く
                        if z_type not in self.VALID_ZONE_TYPE:
                            raise ParserError(
                                f"Line {i}: Invalid zone type \"{z_type}\". "
                                f"Allowed types are {self.VALID_ZONE_TYPE}")

                        # start, endのcapacityはinf, その他はdefault=1.0
                        is_start_or_end = z_prefix in ("start_hub", "end_hub")
                        try:
                            max_drones = (
                                math.inf
                                if is_start_or_end
                                else float(meta.get("max_drones", 1.0)))
                            # start, end以外のcapacityの数が0以下なら弾く
                            if not is_start_or_end and max_drones <= 0.0:
                                raise ValueError
                        except ValueError:
                            raise ParserError(
                                f"Line {i}: \"max_drones\" "
                                "must be a positive number.")

                        # Zoneの名前の重複を弾く
                        if name in zones:
                            raise ParserError(
                                f"Line {i}: Duplicate zone name \"{name}\".")

                        # graphにZoneを追加
                        zone = Zone(
                            name=name,
                            x=x,
                            y=y,
                            zone_type=meta.get("zone", "normal"),
                            color=meta.get("color"),
                            max_drones=max_drones
                        )
                        zones[name] = zone

                        # graphにstart_hubを追加
                        if z_prefix == "start_hub":
                            # start_hubか既にある場合を弾く
                            if start_zone:
                                raise ParserError(
                                    f"Line {i}: Multiple start_hub defined.")
                            start_zone = zone

                        # graphにend_hubを追加
                        elif z_prefix == "end_hub":
                            # end_hubか既にある場合を弾く
                            if end_zone:
                                raise ParserError(
                                    f"Line {i}: Multiple end_hub defined.")
                            end_zone = zone

                        continue

                    # ------------------ Connectionの処理 --------------------
                    elif line.startswith("connection:"):
                        # "connection"パターン以外を弾く
                        match = pattern_connection.match(line)
                        if not match:
                            raise ParserError(
                                f"Line {i}: "
                                "Invalid connection format. "
                                "(Zone names cannot contain dashes)")

                        # Connectionの情報を取得
                        name1, name2, meta_str, garbage = match.groups()
                        if garbage and garbage.strip():
                            print(
                                f"{WARNING}Line {i}: "
                                "Ignored trailing characters "
                                f"\"{garbage.strip()}\" "
                                "after metadata.", file=sys.stderr)
                        # メタデータ内にゴミ文字があったら弾く
                        try:
                            meta = self._parse_metadata(
                                    f"[{meta_str}]" if meta_str else "")
                        except ValueError as e:
                            raise ParserError(f"Line {i}: {e}")

                        # connectionのメタデータ以外弾く
                        for key in meta.keys():
                            if key not in self.VALID_CONNECTIONS_KEYS:
                                raise ParserError(
                                    f"Unkown metadata key \"{key}\" "
                                    "for a zone. Allowed keys are "
                                    f"{self.VALID_CONNECTIONS_KEYS}")

                        # Connection上のZoneがまだない時弾く
                        if (name1 not in zones
                                or name2 not in zones):
                            raise ParserError(
                                f"Line {i}: "
                                "Connection refers to undefined "
                                f"zone(s) \"{name1}\" or \"{name2}\"")

                        # 自分自身へのConnectionを弾く
                        if name1 == name2:
                            raise ParserError(
                                f"Line {i}: "
                                "Self-loop connections "
                                f"(like \"{name1}\" and \"{name2}\""
                                " are not allowed)")

                        # Zone同時の重複接続を弾く
                        connection_key = frozenset({name1, name2})
                        if connection_key in self.seen_connections:
                            raise ParserError(
                                f"Line {i}: "
                                "Duplicate connection between "
                                f"\"{name1}\" and \"{name2}\"")
                        self.seen_connections.add(connection_key)

                        # max_link_capacityが1以上の整数ではなければ弾く
                        try:
                            capacity = int(meta.get("max_link_capacity", 1))
                            if capacity <= 0:
                                raise ValueError
                        except ValueError:
                            raise ParserError(
                                f"Line {i}: "
                                "\"max_link_capacity\" "
                                "must be a positive integer.")

                        # graphに追加するConnectionを保存
                        connections_data.append((name1, name2, capacity, i))
                        continue

                    # 該当するフォーマットがない時弾く
                    raise ParserError(
                        f"Line {i}: Unknown directive or syntax error.")

            # map読み込み完了後にstart, endが無い時弾く
            if not start_zone or not end_zone:
                raise ParserError(
                    "Map Validation failed: "
                    "Start or End zone is missing in the map.")

            # Graphを生成
            graph = Graph(nb_drones, start_zone, end_zone)
            # zoneの追加
            for zone in zones.values():
                graph.add_zone(zone)
            # connectionの追加
            for c in connections_data:
                name1, name2, capacity, i = c
                if name1 not in graph.zones or name2 not in graph.zones:
                    raise ParserError(
                        f"Line {i}: "
                        "Connection refers to undefined zone(z) "
                        f"\"{name1}\" or \"{name2}\""
                        )
                graph.add_connection(name1, name2, capacity)

            # 行き止まりを枝刈り
            self._prune_dead_end(graph)
            # Start -> End まで到達可能なマップかチェック
            self._validate_connectivity(graph)

            return graph

        except FileNotFoundError as e:
            raise ValueError(
                f"Required file not found: {filepath}: {e}") from e

        except UnicodeDecodeError as e:
            raise ValueError(
                f"File encoding error (MUST be UTF-8): {filepath}: {e}"
            ) from e

        except PermissionError as e:
            raise ValueError(
                f"Permission denied: {filepath}") from e

        except IsADirectoryError as e:
            raise ValueError(
                f"Path is a directory, not a file: {filepath}") from e

        except OSError as e:
            raise ValueError(
                f"OS error occurred while reading {filepath}: {e}") from e

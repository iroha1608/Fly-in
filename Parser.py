"""
    コマンドラインから受け取った引数をパースし、
    バリデーションのチェックをする。
"""
import re
import math
import argparse
from pathlib import Path
from collections import deque
from pydantic import BaseModel, Field, ValidationError

from Zone import Zone
from Graph import Graph


class CLIConfig(BaseModel):
    """
        コマンドライン引数の情報
    """
    map: Path = Field(
        default=Path("maps/original/test_map.txt"),
        description="Path to the map file"
    )


class ParserError(ValueError):
    """パース中に発生したエラーを行番号とともに保持するカスタムエラー"""
    pass


class Parser:
    """
    """
    def __init__(self) -> None:
        self.graph = Graph()
        self.seen_connections: set = set()
        self.VALID_ZONE_TYPE = {"normal", "blocked", "restricted", "priority"}

    @staticmethod
    def parse_arguments() -> CLIConfig:
        """
            コマンドライン引数をパースし、CLIConfigで検証し返す。
            Returns:
                CLIConfig: パースし検証済みのコマンドライン引数の情報
            Raises:
                ValueError:
                ValidationError:
            """
        parser = argparse.ArgumentParser(description="")

        parser.add_argument(
            "-m", "--map",
            type=str,
            help=""
        )
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
        metadata = {}
        if not metadata_str:
            return metadata

        content_match = re.search(r'\[(.*?)\]', metadata_str)
        if content_match:
            pairs = content_match.group(1).split()
            for pair in pairs:
                if "=" in pair:
                    key, value = pair.split('=', 1)
                    metadata[key] = value

        return metadata

    @staticmethod
    def prune_dead_end(graph: Graph) -> None:
        """
            行き止まりのノードを探索時に含めないように、
            is_pruned = Trueにする。
        """
        while True:
            removed_any = False
            for zone in graph.zones.values():
                # 枝刈り済み、スタート、ゴールはスキップ。
                if zone.is_pruned or zone == graph.start_zone or zone == graph.end_zone:
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

    def _validate_connectivity(self) -> None:
        if not self.graph.start_zone or not self.graph.end_zone:
            raise ParseError(
                "Map validation failed: Missing start_hub or end_hub")

        queue = deque([self.graph.start_zone])
        visited = {self.graph.start_zone.name}

        while queue:
            current = queue.popleft()
            if current == self.graph.end_zone:
                return
            for connection in current.connections:
                target = connection.target_zone
                if (target.name not in visited
                        and target.zone_type != "blocked"
                        and not target.is_pruned):
                    visited.add(target.name)
                    queue.append(target)
        raise ParseError(
            "Map validation failed: "
            "No valid path exists from start_hub to end_hub."
        )

    def parse_file(self, filepath: str) -> Graph:
        pattern_drones = re.compile(r"^nb_drones:\s*(\d+)$")
        pattern_zone = re.compile(r"^(start_hub|end_hub|hub):\s+([^\s\-]+)\s+(-?\d+)\s+(-?\d+)(?:\s+\[(.*?)\])?$")
        pattern_connection = re.compile(r"^connection:\s+([^\s\-]+)-([^\s\-]+)(?:\s+\[(.*?)\])?$")

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for i, line in enumerate(f, 1):
                    line = line.split("#")[0].strip()

                    if not line:
                        continue

                    # "nb_drones"
                    if line.startswith("nb_drones:"):
                        match = pattern_drones.match(line)
                        if not match:
                            raise ParserError(f"Line {i}: Invalid \"nb_drones\" format or negative value.")
                        drones = int(match.group(1))
                        if drones <= 0:
                            raise ParserError(f"Line {i}: \"nb_drones\" must be greater than 0.")
                        self.graph.nb_drones = drones
                        continue

                    # "Zone"
                    if line.startswith(("start_hub:", "end_hub:", "hub:")):
                        match = pattern_zone.match(line)
                        if not match:
                            raise ParserError(f"Line {i}: Invalid zone definition format.")

                        z_prefix, name, x_str, y_str, meta_str = match.groups()
                        x, y = int(x_str), int(y_str)
                        meta = self._parse_metadata(f"[{meta_str}]" if meta_str else "")

                        # zone_type
                        z_type = meta.get("zone", "normal")
                        if z_type not in self.VALID_ZONE_TYPE:
                            raise ParserError(f"Line {i}: Invalid zone type \"{z_type}\". Allowed types are {self.VALID_ZONE_TYPE}")

                        # capacity
                        is_start_or_end = z_prefix in ("start_hub", "end_hub")
                        max_drones = math.inf if is_start_or_end else float(meta.get("max_drones", 1.0))
                        if not is_start_or_end and max_drones <= 0:
                            raise ParserError(f"Line {i}: \"max_drones\" must be a positive number.")

                        # 重複名
                        if name in self.graph.zones:
                            raise ParserError(f"Line {i}: Duplicate zone name \"{name}\".")

                        zone = Zone(
                            name=name,
                            x=x,
                            y=y,
                            zone_type=meta.get("zone", "normal"),
                            color=meta.get("color"),
                            max_drones=max_drones
                        )
                        self.graph.add_zone(zone)

                        if z_prefix == "start_hub":
                            if self.graph.start_zone:
                                raise ParserError(f"Line {i}: Multiple start_hub defined.")
                            self.graph.start_zone = zone

                        elif z_prefix == "end_hub":
                            if self.graph.end_zone:
                                raise ParserError(f"Line {i}: Multiple end_hub defined.")
                            self.graph.end_zone = zone
                        continue

                    # Connection
                    elif line.startswith("connection:"):
                        match = pattern_connection.match(line)
                        if not match:
                            raise ParserError(f"Line {i}: Invalid connection format. (Zone names cannot contain dashes)")

                        name1, name2, meta_str = match.groups()

                        if name1 not in self.graph.zones or name2 not in self.graph.zones:
                            raise ParserError(f"Line {i}: Connection refers to undefined zone(s) \"{name1}\" or \"{name2}\"")

                        # 重複接続
                        connection_key = frozenset({name1, name2})
                        if connection_key in self.seen_connections:
                            raise ParserError(f"Line {i}: Duplicate connection between \"{name1}\" and \"{name2}\"")
                        self.seen_connections.add(connection_key)
                        meta = self._parse_metadata(f"[{meta_str}]" if meta_str else "")

                        # max_link_capacity
                        capacity = int(meta.get("max_link_capacity", 1))
                        if capacity <= 0:
                            raise ParserError(f"Line {i}: \"max_link_capacity\" must be a positive integer.")
                        self.graph.add_connection(name1, name2, capacity)
                        continue

                    raise ParserError(f"Line {i}: Unknown directive or syntax error.")

            if not self.graph.start_zone or not self.graph.end_zone:
                raise ParserError(
                    "Map Validation failed: "
                    "Start or End zone is missing in the map."
                )

            self._validate_connectivity()
            return self.graph

        except FileNotFoundError as e:
            raise ValueError(
                f"Required file not found: {filepath}: {e}") from e

        except UnicodeDecodeError as e:
            raise ValueError(
                f"File encoding error (MUST be UTF-8): {filepath}: {e}") from e

        except PermissionError as e:
            raise ValueError(
                f"Permission denied: {filepath}") from e

        except IsADirectoryError as e:
            raise ValueError(
                f"Path is a directory, not a file: {filepath}") from e

        except OSError as e:
            raise ValueError(
                f"OS error occurred while reading {filepath}: {e}") from e


"""
    コマンドラインから受け取った引数をパースし、
    バリデーションのチェックをする。
"""
import re
import math
import sys
import argparse
from pathlib import Path
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


class Parser:
    """
    """
    def __init__(self) -> None:
        self.graph = Graph()

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
        parser = argparse.ArgumentParser(
            description=""
        )

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

    def parse_file(self, filepath: str) -> Graph:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.split("#")[0].strip()
                    if not line:
                        continue

                    if line.startswith("nb_drones"):
                        self.graph.nb_drones = int(line.split(":")[1].strip())
                        continue

                    if line.startswith(("start_hub:", "end_hub:", "hub:")):
                        parts = line.split(":", 1)[1].strip().split("[", 1)
                        base_info = parts[0].split()
                        name = base_info[0]
                        x, y = int(base_info[1]), int(base_info[2])

                        meta = self._parse_metadata(f"[{parts[1]}]" if len(parts) > 1 else "")

                        is_start = line.startswith("start_hub:")
                        is_end = line.startswith("end_hub:")
                        max_drones = (
                            math.inf
                            if (is_start or is_end)
                            else float(meta.get("max_drones", 1.0))
                        )

                        zone = Zone(
                            name=name,
                            x=x,
                            y=y,
                            zone_type=meta.get("zone", "normal"),
                            color=meta.get("color"),
                            max_drones=max_drones
                        )

                        self.graph.add_zone(zone)
                        if is_start:
                            self.graph.start_zone = zone
                        elif line.startswith("end_hub"):
                            self.graph.end_zone = zone

                    elif line.startswith("connection:"):
                        parts = line.split(":", 1)[1].strip().split("[", 1)
                        name1, name2 = parts[0].strip().split("-")

                        meta = self._parse_metadata(f"[{parts[1]}]" if len(parts) > 1 else "")
                        capacity = int(meta.get("max_link_capacity", 1))

                        self.graph.add_connection(name1, name2, capacity)

                if not self.graph.start_zone or not self.graph.end_zone:
                    raise ValueError(
                        "Start or End zone is missing in the map.")

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


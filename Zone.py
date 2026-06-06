from collections import defautdict
from dataclasses import dataclass, field

from Connection import Connection

class Zone:
    """
        各Zoneの情報、ターン毎の予約状況(reservations)を管理。
    """
    def __init__(
        self, name: str, x: int, y: int,
        zone_type: str = "normal",
        color: str | None = None,
        max_drones: float = 1.0
    ) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.color = color
        self.max_drones = max_drones
        self.reservations: defaultdict[int, int] = defaultdict(int)
        self.connections: list[Connection] = []

    def can_enter(self, turn:int) -> bool:
        """
            指定ターンにZoneに空きがあるか判定。
            Args:
                turn: 指定したターン
            Returns:
                droneの数に余裕があればTrue。
        """
        return self.reservations[turn] < self.max_drones

    def reserve(self, turn: int) -> None:
        """
            指定したターンにZoneを予約。
        """
        self.reservations[turn] += 1

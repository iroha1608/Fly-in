from collections import defautdict

from Zone import Zone


class Connection:
    """
        ZoneのConnection、
        Connectionの予約状況(reservationsとZoneのcapacityの比較)を管理。
    """
    def __init__(self, target_zone: Zone, max_link_capacity: int=1) -> None:
        self.target_zone = target_zone
        self.max_link_capacity = max_link_capacity
        self.reservations: defaultdict[int, int] = defaultdict(int)

    def can_enter(self, turn:int) -> bool:
        """
            指定ターンにZoneに空きがあるか判定。
            Args:
                turn: 指定したターン
            Returns:
                droneの数に余裕があればTrue。
        """
        return self.reservations[turn] < self.max_link_capacity

    def reserve(self, turn: int) -> None:
        """
            指定したターンにConnectionを予約。
            Args:
                turn: 指定したターン
        """
        self.reservations[turn] += 1

from collections import defaultdict

from Zone import Zone
from Connection import Connection


class Graph:
    def __init__(
        self, nb_drones: int,
        start_zone: Zone, end_zone: Zone
    ) -> None:
        """
            nb_drones: 全体のドローンの数
            start_zone: スタート
            end_zone: ゴール
            zones: マップ全体のZoneの辞書
        """
        self.nb_drones: int = nb_drones
        self.start_zone: Zone = start_zone
        self.end_zone: Zone = end_zone
        self.zones: dict[str, Zone] = {}

    def add_zone(self, zone: Zone) -> None:
        """"""
        self.zones[zone.name] = zone

    def add_connection(self, name1: str, name2: str, capacity: int) -> None:
        """
            Zone同士のConnectionを双方向のZoneに追加する。
            Args:
                name1: 1つ目のZone
                name2: 2つ目のZone
                capacity: Connectionのmax_link_capacity
        """
        if name1 in self.zones and name2 in self.zones:
            zone1 = self.zones[name1]
            zone2 = self.zones[name2]

            two_way_reservations: defaultdict[int, int] = defaultdict(int)

            connection1 = Connection(zone2, capacity)
            connection1.reservations = two_way_reservations
            zone1.connections.append(connection1)

            connection2 = Connection(zone1, capacity)
            connection2.reservations = two_way_reservations
            zone2.connections.append(connection2)

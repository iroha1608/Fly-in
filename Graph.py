from collections import defaultdict

from Zone import Zone
from Connection import Connection


class Graph:
    """
    """
    def __init__(self) -> None:
        self.nb_drones: int = 0
        self.start_zone: Zone | None = None
        self.end_zone: Zone | None = None
        self.zones: dict[str, Zone] = {}

    def add_zone(self, zone: Zone) -> None:
        self.zones[zone.name] = zone

    def add_connection(self, name1: str, name2: str, capacity: int) -> None:
        if name1 in self.zones and name2 in self.zones:
            zone1 = self.zones[name1]
            zone2 = self.zones[name2]

            two_way_reservations = defaultdict(int)
            connect1 = Connection(zone2, capacity)
            connect1.reservations = two_way_reservations
            zone1.connections.append(Connection(connect1)

            connect2 = Connection(zone1, capacity)
            connect2.reservations = two_way_reservations
            zone2.connections.append(Connection(connect2))

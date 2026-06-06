from Zone import Zone
from Connection import Connection

class Gragh:
    """
    """
    def __init__(self) -> None:
        self.nb_drones: int = 0
        self.start_zone: Zone | None = None
        self.end_zone Zone | None = None
        self.zones: dict[str, Zone] = {}

    def add_zone(self, zone: Zone) -> None:
        self.zones[zone.name] = zone

    def add_connection(self, name1: str, name2: str, capacity: int) -> None:
        if name1 in self.zones and name2 in self.zones:
            zone1 = self.zones[name1]
            zone2 = self.zones[name2]
            zone1.connections.append(Connection(zone2, capacity))
            zone2.connections.append(Connection(zone1, capacity))

"""Graph Class for managing zones and connections in a drone simulation."""
from collections import defaultdict

from Zone import Zone
from Connection import Connection


class Graph:
    """Graph Class

   Graph Class for managing zones and connections in a drone simulation.

    Attributes:
        nb_drones (int): Number of drones in the simulation.
        start_zone (Zone): The starting zone for the drones.
        end_zone (Zone): The ending zone for the drones.
        zones (dict[str, Zone]):
            A dictionary mapping zone names to Zone objects.
        connections (dict[str, Connection]):
            A dictionary mapping connection names to Connection objects.

    """
    def __init__(
        self, nb_drones: int,
        start_zone: Zone, end_zone: Zone
    ) -> None:
        """Graph Class for managing zones and connections in a simulation.

        Args:
            nb_drones (int): Number of drones in the simulation.
            start_zone (Zone): The starting zone for the drones.
            end_zone (Zone): The ending zone for the drones.

        """
        self.nb_drones: int = nb_drones
        self.start_zone: Zone = start_zone
        self.end_zone: Zone = end_zone
        self.zones: dict[str, Zone] = {}
        self.connections: dict[str, Connection] = {}

    def add_zone(self, zone: Zone) -> None:
        """add_zone adds a Zone object to the graph.

        Args:
            zone (Zone): The Zone object to be added to the graph.

        """
        self.zones[zone.name] = zone

    def add_connection(self, name1: str, name2: str, capacity: int) -> None:
        """add_connection adds a bidirectional connection between two zones.

        Args:
            name1 (str): The name of the first zone.
            name2 (str): The name of the second zone.
            capacity (int):
                The maximum number of drones that can use the connection
                at the same time

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

            self.connections[f"{name1}-{name2}"] = connection1
            self.connections[f"{name2}-{name1}"] = connection2

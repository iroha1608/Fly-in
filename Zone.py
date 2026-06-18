"""Zone Class for representing a location in the drone simulation."""
from collections import defaultdict


class Zone:
    """Zone Class

    Manages the state of a zone in the drone simulation,
    including its properties, reservations, and connections to other zones.

    Attributes:
        name (str): The name of the zone.
        x (int): The x-coordinate of the zone.
        y (int): The y-coordinate of the zone.
        zone_type (str): The type of the zone.
        color (str | None): The color of the zone.
        max_drones (float):
            The maximum number of drones that can be in the zone at once.
        reservations (defaultdict[int, int]):
            A dictionary mapping turns to the number of drones reserved
            for that turn.
        connections (list[Connection]):
            A list of connections from this zone to other zones.
        is_pruned (bool):
            A flag indicating whether the zone has been pruned.

    """
    def __init__(
        self, name: str, x: int, y: int,
        zone_type: str = "normal",
        color: str | None = None,
        max_drones: float = 1.0
    ) -> None:
        """Initializes a Zone object with the given properties.

        Args:
            name (str): The name of the zone.
            x (int): The x-coordinate of the zone.
            y (int): The y-coordinate of the zone.
            zone_type (str, optional):
                The type of the zone. Defaults to "normal".
            color (str | None, optional):
                The color of the zone. Defaults to None.
            max_drones (float, optional):
                The maximum number of drones that can be in the zone at once.
                Defaults to 1.0.
        """
        from Connection import Connection
        self.name = name
        self.x = x
        self.y = y
        self.zone_type = zone_type
        self.color = color
        self.max_drones = max_drones
        self.reservations: defaultdict[int, int] = defaultdict(int)
        self.connections: list[Connection] = []
        self.is_pruned: bool = False

    def can_enter(self, turn: int) -> bool:
        """Zone has available capacity for drones at the specified turn.

        Args:
            turn (int): The turn to check for available capacity.

        Returns:
            bool:
                True if the number of reserved drones is less than the maximum
                allowed, False otherwise.

        """
        return self.reservations[turn] < self.max_drones

    def reserve(self, turn: int) -> None:
        """Reserve a spot in the zone for a drone at the specified turn.

        Args:
            turn (int): The turn for which to reserve a spot in the zone.

        """
        self.reservations[turn] += 1

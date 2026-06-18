"""Connection Class between zones."""
from collections import defaultdict

from Zone import Zone


class Connection:
    """Connection Class

    Manages the state of a connection between two zones
    in the drone simulation, including its target zone, maximum link capacity,
    and reservations.

    Attributes:
        target_zone (Zone): The zone that this connection leads to.
        max_link_capacity (int):
            The maximum number of drones that can use this connection
            at the same time.
        reservations (defaultdict[int, int]):
            A dictionary mapping turns to the number of drones reserved for
            that turn on this connection.

    """
    def __init__(self, target_zone: Zone, max_link_capacity: int = 1) -> None:
        """Initializes a Connection object with the given target zone and
        maximum link capacity.

        Args:
            target_zone (Zone): The zone that this connection leads to.
            max_link_capacity (int, optional):
                The maximum number of drones that can use this connection at
                the same time. Defaults to 1.

        """
        self.target_zone = target_zone
        self.max_link_capacity = max_link_capacity
        self.reservations: defaultdict[int, int] = defaultdict(int)

    def can_enter(self, turn: int) -> bool:
        """Checks if a drone can enter the connection at the specified turn.

        Args:
            turn (int): The turn for which to check availability.

        Returns:
            bool: True if the connection is available, False otherwise.

        """
        return self.reservations[turn] < self.max_link_capacity

    def reserve(self, turn: int) -> None:
        """Reserves the connection for a drone at the specified turn.

        Args:
            turn (int): The turn for which to reserve the connection.

        """
        self.reservations[turn] += 1

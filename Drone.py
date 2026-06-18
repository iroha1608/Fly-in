"""Drone class for the Fly-in System.

This class represents a drone in the system, managing its state and movement.

"""


class Drone:
    """Drone class for the Fly-in System.

    Attributes:
        id (str): The unique identifier for the drone.
        start_location (str): The starting location of the drone.
        color (str | None): The color of the drone, if specified.
        planned_path (list[str]):
            The planned path for the drone, as a list of locations.

    """
    def __init__(
        self, drone_id: str, start_location: str, color: str | None = None
    ) -> None:
        """Initializes a Drone object with the given properties.

        Args:
            drone_id (str): The unique identifier for the drone.
            start_location (str): The starting location of the drone.
            color (str | None, optional):
                The color of the drone, if specified. Defaults to None.

        """
        self.id = drone_id
        self.start_location = start_location
        self.color = color
        self.planned_path: list[str] = []

    def set_path(self, path_history: list[str]) -> None:
        """Sets the planned path for the drone.

        Args:
            path_history (list[str]):
                The planned path for the drone, as a list of locations.

        """
        self.planned_path = path_history

    def get_location(self, turn: int) -> str:
        """Returns the location of the drone at the specified turn.

        Args:
            turn (int): The turn number for which to get the drone's location.

        Returns:
            str: The location of the drone at the specified turn.

        """
        if turn <= 0:
            return self.start_location

        # 既にゴールに到達している時、最終地点に留まる。
        if turn > len(self.planned_path):
            return self.planned_path[-1]

        return self.planned_path[turn - 1]

    def has_moved(self, turn: int) -> bool:
        """Checks if the drone has moved at the specified turn.

        Args:
            turn (int): The turn number to check for movement.

        Returns:
            bool: True if the drone has moved, False otherwise.

        """
        if turn <= 0 or not self.planned_path:
            return False

        # 既にゴールに到達している時、待機とする。
        if turn > len(self.planned_path):
            return False

        current_location = self.get_location(turn)
        previous_location = self.get_location(turn - 1)

        return current_location != previous_location

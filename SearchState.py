"""PathFinding SearchState class for the Fly-in System.

This class represents the state of the search during pathfinding.
It includes the current cost, turn number, current zone, path history,
and visited zones.

"""
from dataclasses import dataclass, field

from Zone import Zone


@dataclass(order=True)
class SearchState:
    """PathFinding SearchState class for the Fly-in System.

    Attributes:
        cost (float): The current cost of the path.
        turn (int): The current turn number.
        current_zone (Zone): The current zone in the pathfinding process.
        path_history (list[str]): The history of zones visited in the path.
        visited_zones (set[str]): A set of zones that have been visited.

    """
    cost: float
    turn: int = field(compare=False)
    current_zone: Zone = field(compare=False)
    path_history: list[str] = field(compare=False)
    visited_zones: set[str] = field(compare=False)

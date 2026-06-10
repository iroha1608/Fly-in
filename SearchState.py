from dataclasses import dataclass, field

from Zone import Zone


@dataclass(order=True)
class SearchState:
    """
        等価判定(__eq__)の他、特殊メソッド(__lt__)が生成される。
        定義順(cost -> turn -> ...)での比較。
    """
    cost: float
    turn: int = field(compare=False)
    current_zone: Zone = field(compare=False)
    path_history: list[str] = field(compare=False)

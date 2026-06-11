class Drone:
    """
        各ドローンの状態を管理するクラス。
        ID, 経路, 現在地, 表示色
    """
    def __init__(
        self, drone_id: str, start_location: str, color: str | None = None
    ) -> None:
        self.id = drone_id
        self.start_location = start_location
        self.color = color
        self.planned_path: list[str] = []

    def set_path(self, path_history: list[str]) -> None:
        """
            PathFinderで計算した経路をドローンごとの予定表として登録する。
        """
        self.planned_path = path_history

    def get_location(self, turn: int) -> str:
        """
            ドローンの指定したターンの位置を取得する。
            ターン1=index 0
        """
        if turn <= 0:
            return self.start_location

        # 既にゴールに到達している時、最終地点に留まる。
        if turn > len(self.planned_path):
            return self.planned_path[-1]

        return self.planned_path[turn - 1]

    def has_moved(self, turn: int) -> bool:
        """
            ドローンが指定したターンで移動しているか判定する。
        """
        if turn <= 0 or not self.planned_path:
            return False

        # 既にゴールに到達している時、待機とする。
        if turn > len(self.planned_path):
            return False

        current_location = self.get_location(turn)
        previous_location = self.get_location(turn - 1)

        return current_location != previous_location

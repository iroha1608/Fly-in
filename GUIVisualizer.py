"""tkinterを使用してGUIに描画するGUIVisualizerを提供"""
import tkinter as tk
import math
from typing import Any

from Graph import Graph
from Drone import Drone


class GUIVisualizer:
    """
    """
    def __init__(self, graph: Graph, drones: list[Drone]) -> None:
        self.graph = graph
        self.drones = drones

        self.current_turn = 0
        self.max_turns = (
            max(len(d.planned_path) for d in drones) if drones else 0)

        # アニメーション設定
        # 1ターンの合計時間: 500ms
        self.turn_duration_ms = 800
        # フレームレート
        self.fps = 60
        # 1フレームあたりの待機時間: 16msくらい
        self.frame_delay = int(1000 / self.fps)
        # 現在のターンにおける進行フレーム
        self.current_frame = 0
        self.total_frames_per_turn = int(
            (self.turn_duration_ms / 1000) * self.fps
        )
        self.turn_pause_ms = 400

        # メインウィンドウの作成
        self.root = tk.Tk()
        self.root.title("Fly-in Simulatier")
        self.root.geometry("1200x800")
        self.root.configure(bg="#2D2D2D")

        self.cw, self.ch = 1600, 1200
        self.canvas = tk.Canvas(
            self.root,
            width=self.cw,
            height=self.ch,
            bg="#1E1E1E",
            highlightthickness=0
        )
        self.canvas.pack(pady=20)

        self.turn_label = tk.Label(
            self.root,
            text="Turn: 0",
            font=("Helvetica", 16, "bold"),
            fg="white",
            bg="#2D2D2D"
        )
        self.turn_label.pack()

        self.drone_shapes = {}

        self.tk_colors = {
            "red": "#FF3C3C",
            "green": "#32DC64",
            "blue": "#2878FF",
            "yellow": "#FFD200",
            "magenta": "#EB3CEB",
            "cyan": "#28D2E6",
            "gray": "#828282",
            "orange": "#FF8C00",
            "purple": "#8C28E6",
            "brown": "#964B00",
            "lime": "#78FF00",
            "maroon": "#800000",
            "darkred": "#8B0000",
            "crimson": "#DC143C",
            "pink": "#FF69B4",
            "black": "#444444",
            "gold": "#FFD700",
            "white": "#FFFFFF"
        }
        self._calculate_scale_and_offset()

    def _calculate_scale_and_offset(self) -> None:
        """
            Zoneのすべての(x, y)座標を見て、Canvasの80%に収める。
        """
        if not self.graph.zones:
            self.scale = 100
            self.offset_x, self.offset_y = self.cw / 2, self.ch / 2
            return

        xs = [z.x for z in self.graph.zones.values()]
        ys = [z.y for z in self.graph.zones.values()]

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        width = max_x - min_x
        height = max_y - min_y

        width = width if width > 0 else 1
        height = height if height > 0 else 1

        # 画面の80%に収まるようにスケールを計算
        scale_x = (self.cw * 0.8) / width
        scale_y = (self.ch * 0.8) / height
        self.scale = min(scale_x, scale_y)

        # 中心が画面の真ん中に来るようにoffsetを計算
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        self.offset_x = (self.cw / 2) - (center_x * self.scale)
        self.offset_y = (self.ch / 2) - (center_y * self.scale)

    def _get_pixel_coords(
        self, logical_x: float, logical_y: float
    ) -> tuple[float, float]:
        px = self.offset_x + (logical_x * self.scale)
        py = self.offset_y + (logical_y * self.scale)
        return px, py

    def _get_tk_color(self, color_name: str) -> str:
        """
            文字列のカラーからtkinter用のカラーを取得する。
        """
        if not color_name:
            return "#444444"

        return self.tk_colors.get(color_name.lower(), "#444444")

    def _get_location_coords(self, location_name: str) -> tuple[float, float]:
        if "-" in location_name:
            name1, name2 = location_name.split("-")
            z1, z2 = self.graph.zones[name1], self.graph.zones[name2]
            px1, py1 = self._get_pixel_coords(z1.x, z1.y)
            px2, py2 = self._get_pixel_coords(z2.x, z2.y)

            # restrictedでConnection上で待機している場合は中間に表示
            px = (px1 + px2) / 2
            py = (py1 + py2) / 2

        else:
            zone = self.graph.zones[location_name]
            px, py = self._get_pixel_coords(zone.x, zone.y)

        return px, py

    def draw_map(self) -> None:
        # Connectionの描画
        drawn_connections = set()
        for zone in self.graph.zones.values():
            px1, py1 = self._get_pixel_coords(zone.x, zone.y)

            for connection in zone.connections:
                target = connection.target_zone
                connection_id = tuple(sorted([zone.name, target.name]))
                if connection_id not in drawn_connections:
                    px2, py2 = self._get_pixel_coords(target.x, target.y)

                    line_color = (
                        "#333333"
                        if zone.is_pruned or target.is_pruned
                        else "#666666"
                    )
                    self.canvas.create_line(
                        px1, py1, px2, py2, fill=line_color, width=2
                    )
                    drawn_connections.add(connection_id)

        # Zoneの描画
        r = 20
        for zone in self.graph.zones.values():
            px, py = self._get_pixel_coords(zone.x, zone.y)
            if zone.is_pruned:
                self.canvas.create_oval(
                    px - r,
                    py - r,
                    px + r,
                    py + r,
                    outline="#333333",
                    fill="#222222"
                )
            else:
                color =self._get_tk_color(zone.color)
                self.canvas.create_oval(
                    px - r,
                    py - r,
                    px + r,
                    py + r,
                    outline="#FFFFFF",
                    fill=color, width=2
                )
                self.canvas.create_text(
                    px,
                    py - 20,
                    text=zone.name,
                    fill="#AAAAAA",
                    font=("Helvetica", 8)
                )

    def init_drones(self) -> None:
        start_coords = self._get_location_coords(self.graph.start_zone.name)
        r = 5

        for drone in self.drones:
            shaped_id = self.canvas.create_oval(
                start_coords[0] - r,
                start_coords[1] - r,
                start_coords[0] + r,
                start_coords[1] + r,
                fill="#00FFFF",
                outline="white"
            )
            self.drone_shapes[drone.id] = shaped_id

    def animate_turn(self) -> None:
        """
            1ターンごとの状態を画面に反映、次のターンをスケジュールする。
            60FPSで500msのターン
        """
        # アニメーション終了判定
        if self.current_frame >= self.total_frames_per_turn:
            self.current_frame = 0
            self.current_turn += 1

            if self.current_turn > self.max_turns:
                self.turn_label.config(text=f"Turn: {self.max_turns} (Finished)")
                return
            self.turn_label.config(f"Turn: {self.current_turn}")
            # 指定した時間分待ってから再開
            self.root.after(self.turn_pause_ms, self.animate_turn)
            # 一旦returnし、afterによる呼び出しを待つ
            return

        # 進捗率 0.0 -> 1.0
        progress = self.current_frame / self.total_frames_per_turn
        # イージング関数(なめらかな加減速: easeInOutQuad)
        eased_progress = progress * progress * (3 - 2 * progress)

        r = 5
        for drone in self.drones:
            # 前のターンの位置と今のターンの位置を記憶
            start_location = drone.get_location(self.current_turn - 1)
            end_location = drone.get_location(self.current_turn)

            start_px, start_py = self._get_location_coords(start_location)
            end_px, end_py = self._get_location_coords(end_location)

            # 補完された現在座標を計算
            current_px = start_px + (end_px - start_px) * eased_progress
            current_py = start_py + (end_py - start_py) * eased_progress

            shape_id = self.drone_shapes[drone.id]
            self.canvas.coords(
                shape_id,
                current_px - r,
                current_py - r,
                current_px + r,
                current_py + r
            )

        self.current_turn += 1
        # 次のフレームを描画
        self.root.after(self.frame_delay, self.animate_turn)

    def start(self) -> None:
        """
            Tkinterのメインループの開始。
        """
        self.draw_map()
        self.init_drones()

        # 起動後、1秒待機してからオートプレイ開始
        self.root.after(1000, self.animate_turn)
        self.root.mainloop()

if __name__ == "__main__":
    visualizer = GUIVisualizer()
    visualizer.start()

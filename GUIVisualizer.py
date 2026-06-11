import tkinter as tk
from typing import Any

# from Graph import Graph


class GUIVisualizer:
    """
    """
    def __init__(self, graph: Any | None = None) -> None:
        self.graph = graph

        # メインウィンドウの作成
        self.root = tk.Tk()
        self.root.title("Fly-in Simulatier")
        self.root.geometry("800x600")

        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="#FFFFFF")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.create_text(
            400, 300,
            text="GUI Window Loaded Successfully!\nReady for Drone Simulation.",
            fill="#333333",
            font=("Helvetica", 16, "bold"),
            justify=tk.CENTER
        )

    def start(self) -> None:
        """
            Tkinterのメインループの開始。
        """
        self.root.mainloop()

if __name__ == "__main__":
    visualizer = GUIVisualizer()
    visualizer.start()

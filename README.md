*This project has been created as part of the 42 curriculum by nsato.*

<table>
	<thead>
    	<tr>
      		<th style="text-align:center">English</th>
      		<th style="text-align:center"><a href="README_ja.md">Japanese</a></th>
    	</tr>
  	</thead>
</table>

<h1>
	Fly-in
</h1> <H2>
	Drones are interesting.
</H2>


## 📖*Content*
1. [💡Description](#1-Description)
2. [✅File Structure](#2-File-Structure)
3. [✅Instructions](#2-Instructions)
4. [⛏Additional sections](#3-Additional-sections)
	1. [My algorithm choices and implementation strategy](3-1.-My-algorithm-choices-and-implementation-strategy.)
	2. [Reasons for selecting Dijkstra’s algorithm](#3-2-Reasons-for-selecting-Dijkstra’s-algorithm)
	3. [Visualization features and improved user experience](#3-3-Visualization-features-and-improved-user-experience)
4. [Input and Output Examples](#4-Input-and-Output-Examples)
5. [🎁Bonus](#5-Bonus)
6. [🌈Resources](#6-Resources)
	1. [URL](#6-1-URL)
	2. [AI Usage](#6-2-AI-Usage)


## 💡1. Description
Design and implement an efficient drone routing system that navigates multiple autonomous drones from a central base to a target location through a dynamic network.  
This Python project challenges learners to create a custom pathfinding algorithm that handles simultaneous drone movement while respecting zone occupancy rules, movement costs, and conflict resolution.  
The system must parse complex map files, implement object-oriented design principles, and optimize for minimal simulation turns.  
Learners will develop skills in graph algorithms, concurrent pathfinding, and performance optimization while working with real-world constraints such as restricted zones, bottlenecks, and deadlock prevention.  
(from the project PDF)  

### 📁2. File Structure
```
| - Makefile
| - README.md
| - README_ja.md
| - .images
| - .gitignore
| - .flake8
| - main.py
| - Parser.py
| - Graph.py
| - Zone.py
| - Connection.py
| - PathFinder.py
| - Drone.py
| - SearchState.py
| - SimulationEngine.py
| - TerminalVisualizer.py
| - GUIVisualizer.py
| - ColorManager.py
| - tests
```

## ✅2.Instructions

- If uv is not installed, run the official uv installer script.  
```
make uv-install
```

Or
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

- Run the program using the following command.  
*When using a Makefile, only the default file can be specified.*  
```
make run
```
- To run the program with a specified map file, use the following command:
```
uv run main.py -m <map_file>
```
- To perform code style checks, such as type hints, use the following command:
```
make lint
```
To perform more rigorous checks, use the following command:
```
make lint-strict
```
  
- `make run` automatically sets up a virtual environment.
    If it does not set up, please follow these steps:
1. Set up the virtual environment.  
```
make setup
```
2. Synchronize
```
make install
```
- Other commands are as follows:

- Delete cache files
```
make clean
```
- Delete files, including those in the virtual environment
```
make fclean
```

## ⛏4. Additional Requirements
### 4-1. Algorithm Selection and Implementation Strategy
- Since multiple drones will be moving simultaneously in this project, it is necessary to efficiently calculate the path for each drone.  
- Therefore, we will use graph search algorithms, such as the A* algorithm or Dijkstra’s algorithm, to calculate the shortest path for each drone.  
- The Dijkstra algorithm used in this project is
- Additionally, to avoid collisions between drones, we must take the positions of other drones into account when calculating each drone’s path.  
- Furthermore, we will implement an algorithm to select the optimal path by considering zone occupancy rules and movement costs.  
- As for the implementation strategy, we first parse the map file and construct the graph structure. Next, we set the initial and target positions for each drone and calculate their paths.
- We calculate the path for each drone one at a time, updating the occupancy status of Zones and Connections as we go to avoid collisions.
- Additionally,
- Finally, we run the simulation and visualize the movement of each drone.  

### 4-2. Reasons for Selecting Dijkstra’s Algorithm
- Dijkstra’s Algorithm is a graph theory algorithm that efficiently solves the shortest path problem. It can determine the shortest distance and path from a start node to a goal node.
- In this project, since there are multiple drones moving simultaneously, it is necessary to efficiently calculate the path for each drone. Since Dijkstra’s Algorithm provides an optimal solution for graphs with non-negative edge costs, it is well-suited for route calculation that takes drone movement costs into account.
- Furthermore, Dijkstra’s Algorithm does not require heuristics like the A* algorithm and works effectively even on simple graph structures. This makes it easier to calculate routes that account for drone movement costs and zone occupancy rules.
- Furthermore, the Dijkstra algorithm can efficiently calculate routes for each drone even when multiple drones are moving simultaneously. By calculating the route for each drone one at a time and updating the occupancy status of Zones and Connections as needed, collisions are avoided. This allows for the selection of optimal routes while preventing collisions between drones.

### 4-3. Visualization Features and Improved User Experience
- In this project, we will implement both terminal-based and GUI-based visualization to visually represent drone movements.  
- Terminal-based visualization displays the position of each drone in real time, allowing users to confirm drone movements via text.  
- The GUI visualization displays drone movements as animations, allowing users to intuitively understand the drones’ paths.  
- This enables users to monitor drone movements in real time and intuitively understand the simulation results.
- Additionally, the GUI visualization darkens inaccessible zones, allowing users to intuitively understand the drones’ navigable range.

### 5. Input and Output Examples
- You can specify a map file using `uv run main.py -map <map_file>`.  

- You can view the drone's movements in real time in the terminal.  
- The information displayed in the terminal consists of strings indicating each drone's position;  
for Zone, it is displayed as `D<ID>-<zone>`, and for Connection, as `D<ID>-<connection>`.  

<img src="./.images/terminal.png" width="600"/>

- An example of a map file is shown below.  

<img src="./.images/map.png" width="600"/>

- If you specify a map file as shown above, the GUI will display the drone moving from Start to Goal as shown below.  

<img src="./.images/turn0.png" width="600"/>

- The drone's movement is updated every turn, and its position is displayed in real time.  

<img src="./.images/turn2.png" width="600"/>

- The simulation continues until the drones reach their destination. Finally, the screen displays the state where all drones have reached their destination.  

<img src="./.images/turn4.png" width="600"/>

- You can exit the program by pressing the Escape key, clicking the “X” button in the GUI, or pressing Ctrl+C in the terminal.  

## 🎁6. Bonus
- The condition for the bonus is that the provided map files must be executable within the specified number of turns.
- In this implementation, all map files are now executable within the specified number of turns without the need for any special processing. 

## 🌈7. Resources

### 7-1. URL
[Python defaultdict の使い方](https://qiita.com/xza/items/72a1b07fcf64d1f4bdb7)  
[ダイクストラ法最短経路問題](http://www.deqnotes.net/acmicpc/dijkstra/)  
[初心者のためのダイクストラアルゴリズム](https://qiita.com/knhr__/items/cb3ce311508337128714)  
[tkinter Python Documentation](https://docs.python.org/ja/3.14/library/tkinter.html)  
[GoogleスタイルのPython Docstringの入門](https://qiita.com/11ohina017/items/118b3b42b612e527dc1d)

### 7-2. AI Usage
- Antigravity
    - Compile and review the task list
    - Refactor the code
    - Propose methods needed for GUI implementation and discuss challenges encountered while studying
- Copilot
    - Ensure consistent styling when generating docstrings
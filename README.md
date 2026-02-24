*This project has been created as part of the 42 curriculum by ayhammou, evarache.*

# Description

This project has to goal to allow us to create a maze generator, and display its result in the terminal. The maze must respect some criteria defined previously : the width, the height, the entry and the exit,and if it is perfect (that means that the maze must have only one path) or not.
We chose to add one parameter : whether the maze is displayed with an animation or not.

The programme takes one parameter, the file containing the configuration of the Maze. The file must contain every parameters mentioned above, and have necessarily this format :

												WIDTH=10  
												HEIGHT=9  
												ENTRY=0,1  
												EXIT=5,0  
												OUTPUT_FILE=output_maze.txt  
												PERFECT=False  
												ANIMATE=False  

## Algorithm
We used two distinct algorithms for this project: one to build the maze, and one to solve it.

Generation: Recursive Backtracker (DFS)
Why we chose it: We chose this algorithm because it is easy to implement and naturally creates complex mazes with long, winding corridors and tricky dead ends.
How it works: By default, this algorithm always creates a perfect maze (a maze where there is exactly one unique path between any two points ). If the configuration file asks for an imperfect maze, we simply take this perfect maze and break down a few extra walls at the end to create loops and multiple possible paths.

Solving: Breadth-First Search (BFS)
Why we chose it: While DFS is great for digging deep into the maze randomly, BFS explores the maze level by level, like a wave of water spreading outwards. We chose it because it mathematically guarantees finding the shortest valid path from the entry to the exit, which is a core requirement of the project.

## Output
The generator create an output file that is used to display the maze. In this output, the maze is represented using one hexadecimal digit per cell, where each digit encodes which walls are closed:
| Bits | Direction |
|------|-----------|
|  0   |   North   |
|  1   |   East    |
|  2   |   South   |
|  3   |   West    |

A wall being closed sets the bit to 1, open means 0.
Example: 3 (binary 0011) means walls are open to the south and west. Or A
(binary 1010) means that east and west walls are closed.
Cells are stored row by row, one row per line. 
After an empty line, these informations are stored :
- The entry coordinates
- The exit coordinates
- The path from entry to exit, using the four letters N, E, S, W

The output will have this format :

												95696AC47A  
												D53D393953  
												AD12969556  
												C3AEAB8553  
												9445428792  
												A9393AA96A  
												AAAAAC6ABA  
												AAAAC53AAA  
												C6C6D546C6  

												0,1  
												5,0  
												SSESEEENNENN  


## Visual representation

The maze generated will be displayed in the terminal, with the patern 42 in this center if the size is at least 10x10. The output generated will be parsed and interpreted to allow the display.

## Animation

If in the config file the parameter animate is set at True, the maze will be generate with an animation, that will display every path and wall creation.

## Reusability

The entire maze generation logic is decoupled from the terminal viewer and acts as a standalone, reusable Python package. The package is named mazegen and can be easily imported into any future project.
You can build and install the package locally from the root of this repository:  
```python3 -m build```  
```pip install dist/mazegen-1.0.0-py3-none-any.whl```

**Usage Example:**  
Here is a basic example of how to instantiate the generator, pass custom parameters (like size and perfect), and access both the generated structure and the path solution:

1. Use this command :  
```from mazegen.generator import MazeGenerator```

2. Instantiate the generator with custom parameters :  
```generator = MazeGenerator(width=20, height=15, perfect=True)```

3. Add colors list :  
```list_colors = ["\033[34m██\033[0m", "\033[97m██\033[0m", "\033[90m██\033[0m", "\033[95m██\033[0m", "\033[91m██\033[0m", "\033[38;5;90m██\033[0m"]```

4. Access the generated structure :  
```maze_grid = generator.generate(list_colors, animate=False)```

5. Access the solution :  
```path_solution = generator.solve(x_start=0, y_start=1, x_end=19, y_end=13)```

6. Print the path :  
```print(f"Shortest path found: {path_solution}")```

# Instructions

Previously to run the program, it is necessary to install all the requirements with this command :  
`make install`

The program can be run with with command :  
`make`

To run it in debug mode :  
`make debug`

To clean the project and remove all python temporaly files :  
`make clean`

To run the project with flake8 and mypy :  
`make lint`


# Team and project management


## Roles of each team member : 

|       ayhammou       |       evarache       |
|----------------------|----------------------|
| parsing config       | parsing output       |
| generator algorithm  | terminal rendering   |
| reusability          | display menu         |
| visual animation     | colors management    |


## Planning

Initially, we planned to work sequentially (first building the generation engine, then coding the visual rendering). However, to be more efficient, our planning quickly evolved into a parallel workflow. One team member focused purely on the back-end (generation logic, math, solving, reusability) while the other focused on the front-end (terminal rendering, colors, menus, animation). We defined a strict data format early on so both parts could communicate smoothly.


## Balance-sheet

**What worked well:**  
We had a good communication and a good assiduity on this project, that allow us to be efficient and finish it quickly. Decoupling the generation logic from the visual rendering worked perfectly. Using a simple text output format (hexadecimal strings) as a bridge between the backend generator and the frontend viewer allowed us to test and debug our modules independently without breaking each other's code.

**What could be improved:**   
We could improve our commun work, like work with pair programming, and have more thinking together. That could allow us to have a better harmoniation of our code.
Merging the visual path-drawing with the logical solving string ("SSS...") required some last-minute logic adjustments to match the 2x2 cell visual scale in the terminal. Better anticipating the translation from logical grid coordinates to visual rendering scale early on would have saved us some debugging time.


## Specific tools

We used mypy to check typing errors.

# Resources

w3schools : https://www.w3schools.com/python/default.asp  
Python documentation : https://docs.python.org/3/  

AI was used to create the panel of the colors for display.

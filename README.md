_This project has been created as part of the 42 curriculum by ayhammou, evarache_.

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
--------------------------------------------TO DO------------------------------------------
The maze generation algorithm you chose.
• Why you chose this algorithm.


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

The maze generated will be displayed in the terminal, with the patern 42 in this center, if the size is at least 10x10. The output generated will be parsed and interpreted to allow the display.

## Animation

If in the config file the parameter animate is set at True, the maze will be generate with an animation, that will display every path and wall creation.

## Reusability
-----------------------------------------------TO DO-----------------------------------------------  
What part of your code is reusable, and how.


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
-------------------------------------------------TO DO-----------------------------------------------  
◦ Your anticipated planning and how it evolved until the end
◦ What worked well and what could be improved

## Specific tools

We used mypy to check typing errors.

# Resources

w3schools : https://www.w3schools.com/python/default.asp
Python documentation : https://docs.python.org/3/

AI was used to create the panel of the colors for display.
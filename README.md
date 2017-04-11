# toyrobot
Simple toy robot exercise in python


Application that can read in commands of the following form:

    PLACE X,Y,F
    MOVE
    LEFT
    RIGHT
    REPORT
    
**PLACE** will put the toy robot on the table in position X,Y and facing **NORTH, SOUTH, EAST** or **WEST**. 

The origin (0,0) can be considered to be the **SOUTH WEST** most corner. The first valid command to the robot is a **PLACE** command, after that, any sequence of commands may be issued, in any order, including another **PLACE** command. The application should discard all commands in the sequence until a valid **PLACE** command has been executed. 

**MOVE** will move the toy robot one unit forward in the direction it is currently facing.

**LEFT** and **RIGHT** will rotate the robot 90 degrees in the specified direction without changing the position of the robot. . 

**REPORT** will announce the X,Y and F of the robot. This can be in any form, but standard output is sufficient.

A robot that is not on the table can choose the ignore the **MOVE, LEFT, RIGHT** and **REPORT** commands. Input can be from a file, or from standard input.

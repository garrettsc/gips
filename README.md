# GIPS - grbl Interactive Programming System

A cross platform GRBL CNC controller interface.


# Release 0.1 Features:
1) Connect to grbl - Done
2) Display serial communication - In progress
3) View and set grbl parameters - In progress
4) X,Y,Z DRO - In Progress
5) Home - In Progress
6) Jog - In Progress
7) Stream gcode from file - Soon
8) Current state - In Progress

## Current 0.1 Release Status / Immediate To-Dos:

Slow but steady progress to a semi-stable release. currently no gcode streaming, however
the backbone structure is there for message streaming. Before moving onto message streaming
there are a few stability and code readability issues to address.

1) grbl settings reading, writing, and saving.
2) Jogging needs a default feed rate (and units)
3) DRO format needs nailed down (aligning decimals)
4) Proper exit plan (thread shutdown, killing any hanging zmq recv methods)
5) Remove the 'group box' from widgets to decrease widget footprint
6) Consider using QWidget as the base class in place of QGridLayout

## Display serial communication
Next steps involve parsing the grbls output.
1) Machine state < >
2) Machine position < >
3) Work position < >
4) Planner Buffer count < >
5) RX Buffer load < >
6) GRBL settings $
7) ok messages 
8) feedback messages [ ]



### Contributing:

- Test out the program! Find bugs and report them in detail
- calling Qt, zmq, and grbl folks to examine and suggest improvements








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



# Current 0.1 Release Candidate Status / Immediate To-Dos:

## Grbl Settings
Backbone for grbl settings widget started.
[X] - Load settings from grbl
[X] - Save settings to a file
[X] - Send updated settings to grbl
[ ] - Load settings from a file
[ ] - Display units
[ ] - Highlight items that have been changed?

## Jogging
The jogging seems to work pretty well, however some fine tuning with jog distance as a function of feed needs to be done.
Currently no optimization of the buffer which seems to slow down status requests.
[X] - Jog x,y,z independently
[X] - Jog feed rate
[ ] - Jog distance / feed rate optimization

## DRO
The digital read out is currently very basic and only displays machine coordinates. There is currently no proper string formatting
with leads to misaligned decimal places and auto-resizing of the widget as the numbers grow.
[X] - Display machine coordinates
[ ] - Switch between machine and work coordinates OR display both
[ ] - Format strings to keep decimal places aligned
[ ] - Display current units

## Program Exit
The way the program is setup now does not lend itself well to a clean exit. This mostly has to do the messageManager thread
and the open serial port. This could be fixed in a few ways...
[ ] - Eliminate the use of threading library and use PySides native threading capability
[ ] - Add another message service (Zmq or Queue) to give shutdown request to thread / serial port
[ ] - Add signals / slots (This is probably the best way to go...)

## Switching QGridLayout for QWidget
This isn't a huge priority, mostly because it doesn't really seem to effect performance or development. I'm mostly
considering doing this because it appears that this is more or less the convention when making your own Widgets...

## Widget Enable / Disable Feature
This would most likely have to also include additional signals which could potential be a tedious amount of work. It would be
convienent to have a setAllButtonStates() method in each widget so its easy to active / deactive all buttons in a certain category.

## G-code streaming
Developing ideas....

## Signals / Slots
....


### Contributing:

- Test out the program! Find bugs and report them in detail
- calling Qt, zmq, and grbl folks to examine and suggest improvements

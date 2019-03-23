# GIPS - grbl Interactive Programming System



# Release 0.1 Features:
1) Connect to grbl - Done
2) Display serial communication - In progress
3) View and set grbl parameters - In progress
4) X,Y,Z DRO - Soon
5) Home
6) Jog
7) Stream gcode from file
8) Current state

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


## General notes / brainstorms for grbl serial communication

1) select port
2) Click connect
3) Wait for response (Timeout after so many seconds?)
4) Start serial manager loop

From the grbl documentation, sending a command to grbl proceeds as follows:

1)  Command is sent and one of the following occurs
2a) An error message is thrown indicating the command is not accepted
2b) Grbl responds with additional information followed by an 'ok' message

The serial manager loop is the single piece of code responsible for reading and writing serial data. Having a single
loop responsible for serial communication prevents the program from attempting to read or write to the port at the same time.
The Loop should have very basic functionality.

Listen for unsolicited messages. These include:
- Welcome Message
- Alarm Message
- Any others....

Send a message and wait for an 'ok'.

### Message Categories:

Response Messages:
- [ok] - Message recieved, understood, and acted or will be acted upon
- [error] - Message recieved, however there was an error and the message will be purged and not acted upon

Push Messages:
- < > - Status report
- Grbl X.Xx ['$' for help] - Welcome message after initialization
- ALARM:x - Alarm message
- Several others that can be found on grbls wiki



- System command '$' commands
- ok
- error
- alarm
- 


### Contributing:

- Test out the program! Find bugs and report them in detail
- calling Qt, zmq, and grbl folks to examine and suggest improvements
-
- 







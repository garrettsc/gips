
import zmq
import serial.tools.list_ports
import json
import time

"""
Name:   serialManager.py

Description:

    serialManager.py is the singular point for reading and writing to grbl via
    serial port. 

    The first block reads in any unsolicited messages from grbl, such as startup messages
    and alarms.

    The second block checks if any messages are queued up to be sent to grbl.
    If a message has been 'requested' to be sent, the message will be sent to grbl. The 
    serial manager will read the 'reply' from grbl until either an 'ok' or
    'error' message is recieved. Once the 'ok' or 'error' is recieved, the entire
    reply message is sent back to the entity that requested the message be sent.
"""

#### Realtime commands ####

hexList = {'&JOGCANCEL':0x85,
           '&FO':0x91,
           '&SD':0x84,              #Safety Door
           '&F100':0x90,            #Feed 100%
           '&FP10':0x91,            #Increase Feed 10%
           '&FM10':0x92,            #Decrease Feed 10%
           '&FP01':0x93,            #Increase Feed 1%
           '&FM01':0x94,            #Decrease Feed 1%
           '&R100':0x95,            #Rapid 100%
           '&R50' :0x96,            #Rapid 50%
           '&R25' :0x97,            #Rapid 25%
           '&S100':0x99,            #Spindle 100%
           '&SP10':0x9A,            #Increase Spindle 10%
           '&SM10':0x9B,            #Decrease Spindle 10%
           '&SP01':0x9C,            #Increase Spindle 1%
           '&SM01':0x9D,            #Decrease Spindle 1%
           '&S00' :0x9E,            #Toggle Spindle Stop
           '&TFC' :0xA0,            #Toggle Flood Coolant
           '&TMC' :0xA1}            #Toggle Mist Coolant   


######## ZMQ Request / Reply port ########
serialManagerPort = 5001
alarmState = False
    
def readFromSerial(ser,socket):
    
    message = ser.readline().rstrip()

    if 'ALARM' in message:
        return 2, message       # An alarm was encountered

    elif 'error' in message:
        return 1, message       # An error was encountered

    else:
        return 0, message       # Grbl returned an 'ok'


def readReply(ser,socket):
    """
    This method reads the serial buffer until grbl proper conditions are met
    """
    state, message = readFromSerial(ser,socket)
    fullReplyList = [message]

    while state == 0 and not 'Hold' in message and not 'ok' in message:
        state, message = readFromSerial(ser,socket)
        fullReplyList.append(message)
        
        if message == 'ok':
            break

    return state, fullReplyList

        

def messageManager(ser,unQuereiedMessages):
    
    #Create and bind to zmq port for request / reply messages
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:{}".format(serialManagerPort))
    
    state = 0
    while ser.is_open:
        try:
            #Check incomming unsolicited messages
            while ser.in_waiting:
                state, message = readFromSerial(ser,socket)     #Read any unsolicited messages in the buffer
                unQuereiedMessages.put(message)                 #Put messages into queue for the serial monitor

                if state == 2:                                  #If any of the messages resulted in
                    continue                                    #an alarm state, continue

            #Send outbound messages
            try:
                outgoingMessage = socket.recv_string(flags=zmq.NOBLOCK)

                if state in [0,1]:                              #If normal or error state

                    if outgoingMessage[0] == '&':
                            ser.write(chr(hexList[outgoingMessage]))
                            ser.write('\n')                     #Not sure if this is required for extended ascii
   
                    else:
                        if not outgoingMessage == '?':
                            print outgoingMessage
                        ser.write("{}\n".format(outgoingMessage))
                        

                else:                                           #If in alarm state, only accept these commands

                    if outgoingMessage in ['$H','$h','$X','$x']:
                        ser.write('{}\n'.format(outgoingMessage))

                state, replyMessageList = readReply(ser,socket)        #Get grbls response 'state' and message.
                                                                        # State 0 - ok
                                                                        # State 1 - error
                                                                        # State 2 - Alarm

                reply = json.dumps((state,"\n".join(replyMessageList)))
                socket.send(reply)

            except zmq.Again as e:
                pass #No outgoing messages
        except:
            pass #Some error occured with serial

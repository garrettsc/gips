
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
    If a message has been 'requested', the message will be sent to grbl. The 
    serial manager will read the 'relpy' from grbl until either an 'ok' or
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

def messageManager(ser,unQuereiedMessages):
    readFromSerial()
    #Create and bind to zmq port for request / reply messages
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:{}".format(serialManagerPort))

    while ser.is_open: 

        try:
            while ser.in_waiting:
                incommingMessage = ser.readline().rstrip()
                unQuereiedMessages.put(incommingMessage)

            try:
                outgoingMessage = socket.recv_string(flags=zmq.NOBLOCK)
                
                if outgoingMessage[0] == '&':
                    ser.write(chr(hexList[outgoingMessage]))
                    ser.write('\n')
                
                else:
                    ser.write("{}\n".format(outgoingMessage))

                fullResponse = ''
                responseMessage = ser.readline().rstrip()

                if 'ALARM' in responseMessage:
                    reply = [None,responseMessage]
                    socket.send(json.dumps(reply))
                    continue
        
                while responseMessage != 'ok' and not 'error' in responseMessage and not 'Hold' in responseMessage:
                    if len(responseMessage) > 0:
                        fullResponse += responseMessage + "\n"
                    responseMessage = ser.readline().rstrip()

                    if 'ALARM' in responseMessage:
                        time.sleep(1)
                        break

 
                if 'Hold' in responseMessage:
                    reply = [responseMessage,'ok']
                
                else:
                    okError = responseMessage
                    reply = [fullResponse,okError]

                socket.send(json.dumps(reply))
            
            except zmq.Again as e:
                pass
        except:
            pass

    
def readFromSerial(ser,socket):
    
    message = ser.readline().rstrip()

    if 'ALARM' in message:
        # socket.send(json.dumps(message))
        return 2, message 

    elif 'error' in message:
        # socket.send(json.dumps(message))
        return 1, message

    else:
        return 0, message


def readReply(ser,socket):
    
    state, message = readFromSerial(ser,socket)
    fullReplyList = [message]
    # print fullReplyList

    while state == 0 and not 'Hold' in message and not 'ok' in message:
        state, message = readFromSerial(ser,socket)
        fullReplyList.append(message)
        
        if message == 'ok':
            break

    return state, fullReplyList

        

def messageManager2(ser,unQuereiedMessages):
    
    #Create and bind to zmq port for request / reply messages
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:{}".format(serialManagerPort))
    
    state = 0
    while ser.is_open:
        try:


            #Check incomming messages
            while ser.in_waiting:
                state, message = readFromSerial(ser,socket)     #Read any unsolicited messages in the buffer
                unQuereiedMessages.put(message)                 #Put messages into queue

                if state == 2:                                  #If any of the messages resulted in
                    continue                                    #an alarm state, continue

            #Send outbound messages
            try:
                outgoingMessage = socket.recv_string(flags=zmq.NOBLOCK)

                if state in [0,1]:                              #If normal or alarm state

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
                # print replyMessageList
                reply = json.dumps((state,"\n".join(replyMessageList)))
                socket.send(reply)

            except zmq.Again as e:
                pass #No outgoing messages
        except:
            pass #Some error occured with serial

    

    



    # Read the serial buffer until newline
    # If the message is not an ALARM or ERROR, return the string
    # If the message is an ERROR, reply to the sender that an error has occured and continue
    # If the message is an ALARM, reply to the sender


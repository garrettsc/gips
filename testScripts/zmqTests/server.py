import zmq
import time


port = 5001

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)

while True:
    message = socket.recv()
    print("Recieved request: {}".format(message))

    socket.send_string("Message Recieved")
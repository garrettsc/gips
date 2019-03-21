import zmq
import threading
import time

def worker(i):

    port = 5001
    context = zmq.Context()
    print "Connecting to server..."
    socket = context.socket(zmq.REQ)
    socket.connect ("tcp://localhost:%s" % port)
    #  Do 10 requests, waiting each time for a response
    for request in range (1,10):
        print "Sending request ", request,"..."
        socket.send_string("Hello from {} - {}".format(i,request))
        #  Get the reply.
        message = socket.recv()
        print "Received reply ", request, "[", message, "]"


threads = 3

for i in range(0,threads):

    print('starting thread {}'.format(i))
    t = threading.Thread(target=worker,args=(i,))
    t.daemon = True
    t.start()
    t.join()

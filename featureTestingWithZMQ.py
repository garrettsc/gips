from PySide.QtGui import QWidget, QPushButton,QHBoxLayout, QApplication, QGridLayout, QLCDNumber, QLabel, QFrame, QTabWidget, QFont, QTextEdit, QComboBox, QFormLayout, QLineEdit, QCheckBox
from PySide.QtCore import QDateTime, QTimer, SIGNAL, QSize, Qt

import zmq

import sys
import serial.tools.list_ports
import time
import threading
import Queue
import json
class MainWindow(QWidget):
    """ Our Main Window class
    """
    def __init__(self):
        """ Constructor Function
        """

        self.serialManagerPort = 5001

        QWidget.__init__(self)
        self.setWindowTitle("grbl Serial Monitor")
        self.setGeometry(100, 100, 1000, 600)

         
    def launch(self):
        """
        This method sets up widgets, layouts, and any other at-runtime services
        """

        self.createQueues()
        self.createSerialMonitor()
        self.createSideMenu()
        self.createCommandSenderMenu()
        self.SetLayout()


##########################################################################################
#=========================== SERIAL MANAGEMENT AND PARSING ===============================
    def serialManager(self):
        """
        This loop is responsible for reading and writing to the serial port.
        
        The first block reads in any unsolicited messages from grbl, such as startup messages
        and alarms.

        The second block checks if any messages are queued up to be sent to grbl.
        If a message has been 'requested', the message will be sent to grbl. The 
        serial manager will read the 'relpy' from grbl until either an 'ok' or
        'error' message is recieved. Once the 'ok' or 'error' is recieved, the entire
        reply message is sent back to the entity that requested the message be sent.

        """

        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:{}".format(self.serialManagerPort))

        while self.ser.is_open:
           
            try:
                while self.ser.in_waiting:
                    incommingMessage = self.ser.readline().rstrip()
                    self.unQuereiedMessages.put(incommingMessage)
                try:
                    outgoingMessage = socket.recv_string(flags=zmq.NOBLOCK)
                    print("OGM: {}".format(outgoingMessage))
                    self.ser.write("{}\n".format(outgoingMessage))
                    fullResponse = ''
                    responseMessage = self.ser.readline().rstrip()

            
                    while responseMessage != 'ok' and not 'error' in responseMessage:
                        fullResponse += responseMessage + "\n"
                        responseMessage = self.ser.readline().rstrip()

                    okError = responseMessage
                    
                    reply = [fullResponse,okError]


                    socket.send(json.dumps(reply))
                
                except zmq.Again as e:
                    pass
            except:
                pass


    

       
    def serialPrinter(self):
        while self.unQuereiedMessages.qsize()>0:
            serialMessage = self.unQuereiedMessages.get()
            self.serialMonitor.append(serialMessage)



    def connectToSerial(self):
        self.serialMonitor.append("Connecting...")

        self.ser = serial.Serial(port=self.portList.currentText(),
                                 baudrate=115200,
                                 timeout=1)

        self.serialMonitor.append("connected to"+self.portList.currentText())

        time.sleep(2)

        t = threading.Thread(target=self.serialManager)
        t.daemon = True
        t.start()

        port = 5001
        context = zmq.Context()
        print "Connecting to server..."
        self.cmdSocket = context.socket(zmq.REQ)
        self.cmdSocket.connect("tcp://localhost:%s" % port)


        # Timer will call two methods every 0.2 seconds
        # 1) Check if any unquerried messages are in the queue to print
        # 2) Request a status update
        self.timer = QTimer(self)
        self.timer.setInterval(200)
        self.connect(self.timer,SIGNAL("timeout()"),self.serialPrinter)
        self.connect(self.timer,SIGNAL('timeout()'),self.requestStatusService)
        self.timer.start()

        

        self.disconnectButton.setEnabled(True)
        self.connectButton.setEnabled(False)


###############################################################################################
###############################################################################################



    def requestStatusService(self):

            self.cmdSocket.send('?')   
            response = self.cmdSocket.recv()
            messageSplit = response.replace('<','').replace('>','').split('|')


            print messageSplit
    
    # def messageParserService(self):
    #     """
    #     The messageParserService method parses through incoming messages and distributes them
    #     to the the appropriate widgets

    #     """

    #     while True:

    #         if self.incommingMessageQ.qsize()>0:
                
    #             #Take a message off the incomming message stack
    #             incomingMessage = self.incommingMessageQ.get()
                
    #             if len(incomingMessage) == 0:
    #                 continue
                

    #             if incomingMessage[0] == '<':   #Status message
    #                 messageSplit = incomingMessage.replace('<','').replace('>','').split('|')
                    
    #                 state = messageSplit[0]
    #                 mPos = messageSplit[1]
    #                 FS = messageSplit[2]
    #             if incomingMessage[0] == '$':   #Settings message
    #                 pass    

    #             else:
    #                 pass

                
    #             self.serialMonitorQ.put(incomingMessage)




#================================================================================================
#################################################################################################




#================================== grbl commands ================================================
##################################################################################################



    def sendHomeCommand(self):
        self.outgoingMessageQ.put("$H")

    def sendUnlockCommand(self):
        self.outgoingMessageQ.put("$X")


    def createQueues(self):
        self.unQuereiedMessages = Queue.Queue()


    def disconnectFromSerial(self):
        self.ser.close()
        self.serialMonitor.append("Disconnected from serial port")
        self.timer.stop()
        self.connectButton.setEnabled(True)
        self.disconnectButton.setEnabled(False)

    def sendCommand(self):
        cmd = self.sendLineEdit.text()
        self.sendLineEdit.clear()
        self.cmdSocket.send_unicode(cmd)
        reply = self.cmdSocket.recv()

        replyList = json.loads(reply)
        fullReplyString = ''.join(replyList)

        self.serialMonitor.append(fullReplyString)



    def createSerialMonitor(self):
        self.serialMonitor = QTextEdit()
        self.serialMonitor.setReadOnly(True)

    def createCommandSenderMenu(self):
        self.sendLineEdit = QLineEdit()
        self.sendButton = QPushButton("Send")
        self.sendButton.clicked.connect(self.sendCommand)
        self.sendLabel = QLabel("Command:")

        self.commandSendLayout = QHBoxLayout()
        self.commandSendLayout.addWidget(self.sendLabel)
        self.commandSendLayout.addWidget(self.sendLineEdit)
        self.commandSendLayout.addWidget(self.sendButton)


    def createSideMenu(self):
        #Side Menu Buttons
        self.connectButton = QPushButton('Connect')
        self.disconnectButton = QPushButton('Disconnect')

        self.homeButton = QPushButton('Home')
        self.unlockButton = QPushButton('Unlock')
        

        #Create COM port combo box
        self.portList = QComboBox()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.portList.addItem(port.device)


        #Connect Buttons:
        self.connectButton.clicked.connect(self.connectToSerial)
        self.disconnectButton.clicked.connect(self.disconnectFromSerial)
        self.homeButton.clicked.connect(self.sendHomeCommand)
        self.unlockButton.clicked.connect(self.sendUnlockCommand)


        #Set Button States
        self.disconnectButton.setEnabled(False)
        self.connectButton.setEnabled(True)




    
    def SetLayout(self):
        gridLayout = QGridLayout()
        
        sideMenuLayout = QGridLayout()

        sideMenuLayout.addWidget(self.connectButton,0,0)
        sideMenuLayout.addWidget(self.disconnectButton,0,1)
        sideMenuLayout.addWidget(self.portList,1,0)
        sideMenuLayout.addWidget(self.homeButton,6,0)
        sideMenuLayout.addWidget(self.unlockButton,6,1)

        gridLayout.addWidget(self.serialMonitor,0,0)
        gridLayout.addLayout(sideMenuLayout,0,1)
        gridLayout.addLayout(self.commandSendLayout,1,0)

        self.setLayout(gridLayout)


if __name__ == '__main__':
    # Exception Handling
    try:
        #QApplication.setStyle('plastique')
        myApp = QApplication(sys.argv)
        mainWindow = MainWindow()

        mainWindow.launch()

        mainWindow.show()
        myApp.exec_()
        sys.exit(0)
    except NameError:
        print("Name Error:", sys.exc_info()[1])
    except SystemExit:
        print("Closing Window...")
    except Exception:
        print(sys.exc_info()[1])
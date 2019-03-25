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
        self.setGeometry(100, 100, 1000, 300)

         
    def launch(self):
        """
        This method sets up widgets, layouts, and any other at-runtime services
        """

        self.createQueues()
        self.createSerialMonitor()
        self.createJogPanel()
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

                    if outgoingMessage == '!':
                        self.ser.write('!')
                    if outgoingMessage[0:2] == '0x':
                        
                        self.ser.write('\x85')
                        self.ser.write('\n')
                        
                    else:
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


#=========================== SERIAL MANAGEMENT AND PARSING ===============================
##########################################################################################
    

       
    def serialPrinter(self):
        while self.unQuereiedMessages.qsize()>0:
            serialMessage = self.unQuereiedMessages.get()
            self.serialMonitor.append(serialMessage)



    def connectToSerial(self):
        """
        This method attempts to open a serial connection to the selected com port.

        """

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
        self.cmdSocket = context.socket(zmq.REQ)
        self.cmdSocket.connect("tcp://localhost:%s" % port)

        self.jogSocket = context.socket(zmq.REQ)
        self.jogSocket.connect("tcp://localhost:%s" % port)

        self.jogCancelSocket = context.socket(zmq.REQ)
        self.jogCancelSocket.connect("tcp://localhost:%s" % port)


        # Timer will call two methods every 0.2 seconds
        # 1) Check if any unquerried messages are in the queue to print
        # 2) Request a status update
        self.timer = QTimer(self)
        self.timer.setInterval(25)
        self.connect(self.timer,SIGNAL("timeout()"),self.serialPrinter)
        self.connect(self.timer,SIGNAL('timeout()'),self.requestStatusService)
        self.timer.start()

        
        self.disconnectButton.setEnabled(True)
        self.connectButton.setEnabled(False)
        self.cmdButtonStates(True)




    def disconnectFromSerial(self):
        self.ser.close()
        self.serialMonitor.append("Disconnected from serial port")
        self.timer.stop()
        self.connectButton.setEnabled(True)
        self.disconnectButton.setEnabled(False)
        self.cmdButtonStates(False)


###############################################################################################
###############################################################################################





###############################################################################################
########################### REQUEST STATUS UPDATE #############################################
    def requestStatusService(self):
        """
        When called send a '?' status update query across the cmd socket and wait for a response.
        Parse out the status and the machine position from the status. Method needs cleaned up significantly
        """

        self.cmdSocket.send('?')   
        response = self.cmdSocket.recv()
        resp = json.loads(response)

        data = resp[0].encode('utf-8')
        status =  data.replace('<','').replace('>','').split('|')[0]
        MPos = data.replace('<','').replace('>','').split('|')[1].split(':')[1].split(',')

        self.droTextWidget.setText(self.droFormat.format(float(MPos[0]),float(MPos[1]),float(MPos[2])))
        self.currentStatusWidget.setText(status)

#================================================================================================
#################################################################################################




#================================== grbl commands ================================================
##################################################################################################

    def sendHomeCommand(self):
        self.cmdSocket.send('$H')
        reply = self.cmdSocket.recv()

    def sendUnlockCommand(self):
        self.cmdSocket.send('$X')
        reply = self.cmdSocket.recv()

    def createQueues(self):
        self.unQuereiedMessages = Queue.Queue()

#================================== grbl commands ================================================
##################################################################################################


    def createJogPanel(self):

        self.pXJogButton = QPushButton()
        

        self.pXJogButton.setText('+X')
        self.pXJogButton.pressed.connect(self.onPress)
        self.pXJogButton.released.connect(self.onRelease)

        self.jogTimer = QTimer()
        self.jogTimer.setInterval(25)
        self.jogTimer.timeout.connect(lambda : self.jogSender(x=0.01,f=1000))



    
    def onPress(self):
        self.jogTimer.start()

    def onRelease(self):
        
        self.jogTimer.stop()
        time.sleep(25/1000.0)

        self.jogCancelSocket.send('!')
        rep = self.jogCancelSocket.recv()
       
        self.jogCancelSocket.send('0x85')
        reply = self.jogCancelSocket.recv()



    # def jogX(self):
    #     jogCmd = '$J=G91X0.5F1500'
    #     self.jogSocket.send(jogCmd)
    #     _ = self.jogSocket.recv()


    def jogSender(self,x=0,y=0,z=0,f=0):
        jogCmd = '$J=G91X{}Y{}Z{}F{}'.format(x,y,z,f)
        self.jogSocket.send(jogCmd)
        self.jogSocket.recv()



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
        ports = serial.tools.list_ports.comports()[::-1]
        for port in ports:
            self.portList.addItem(port.device)


        # Create x,y,z readouts
        self.droTextWidget = QLabel()
        self.droFormat = "X    {:9.4f}\nY    {:9.4f}\nZ    {:9.4f}"
        self.droTextWidget.setText(self.droFormat.format(0,0,0))
        font = QFont()
        font.setPointSize(15)
        self.droTextWidget.setFont(font)


        # Create status label

        self.currentStatusWidget = QLabel()
        self.currentStatusWidget.setFont(font)
        self.currentStatusWidget.setFrameStyle(QFrame.Sunken | QFrame.Panel | QFrame.Box)


        #Connect Buttons:
        self.connectButton.clicked.connect(self.connectToSerial)
        self.disconnectButton.clicked.connect(self.disconnectFromSerial)
        self.homeButton.clicked.connect(self.sendHomeCommand)
        self.unlockButton.clicked.connect(self.sendUnlockCommand)


        #Set Button States
        self.disconnectButton.setEnabled(False)
        self.connectButton.setEnabled(True)
        self.homeButton.setEnabled(False)
        self.unlockButton.setEnabled(False)



    def cmdButtonStates(self,state):
        self.homeButton.setEnabled(state)
        self.unlockButton.setEnabled(state)


    
    def SetLayout(self):
        gridLayout = QGridLayout()
        
        sideMenuLayout = QGridLayout()

        sideMenuLayout.addWidget(self.connectButton,0,0)
        sideMenuLayout.addWidget(self.disconnectButton,0,1)
        sideMenuLayout.addWidget(self.portList,1,0)
        sideMenuLayout.addWidget(self.homeButton,6,0)
        sideMenuLayout.addWidget(self.unlockButton,6,1)
        sideMenuLayout.addWidget(self.droTextWidget,7,0)
        sideMenuLayout.addWidget(self.currentStatusWidget,8,0)
        sideMenuLayout.addWidget(self.pXJogButton,9,0)

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
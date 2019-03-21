from PySide.QtGui import QWidget, QPushButton,QHBoxLayout, QApplication, QGridLayout, QLCDNumber, QLabel, QFrame, QTabWidget, QFont, QTextEdit, QComboBox, QFormLayout, QLineEdit, QCheckBox
from PySide.QtCore import QDateTime, QTimer, SIGNAL, QSize, Qt

import sys
import serial.tools.list_ports
import time
import threading
import Queue
class MainWindow(QWidget):
    """ Our Main Window class
    """
    def __init__(self):
        """ Constructor Function
        """
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
        errors, or alarms.

        The second block checks if any messages are queued up to be sent to grbl.
        If there is a message in the queue it will be sent to grbl and the manager
        will wait for and read any response. The manager will continue to read responses
        until an 'ok' message is recieved

        """
        while self.ser.is_open:
            try:
                while self.ser.in_waiting:
                    incomingMessage = self.ser.readline().rstrip()
                    self.incommingMessageQ.put(incomingMessage)
                
                if self.outgoingMessageQ.qsize()>0:
                    outgoingMessage = self.outgoingMessageQ.get()
                    self.ser.write("{}\n".format(outgoingMessage).encode('utf-8'))
                    
                    #Read GRBLs response - Continue to read until 'ok' is given
                    responseMessage = self.ser.readline().rstrip()
                    
                    if 'ALARM' in responseMessage:
                        self.incommingMessageQ.put(responseMessage)
                        continue

                    while responseMessage != 'ok' and not 'error' in responseMessage:
                        self.incommingMessageQ.put(responseMessage)
                        responseMessage = self.ser.readline().rstrip()
                    self.incommingMessageQ.put(responseMessage)
            except:
                pass

    
    def serialPrinter(self):
        if self.serialMonitorQ.qsize()>0:
            serialMessage = self.serialMonitorQ.get()
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

        t = threading.Thread(target=self.messageParserService)
        t.daemon = True
        t.start()

        t = threading.Thread(target=self.requestStatusService)
        t.daemon = True
        t.start()

        self.timer = QTimer(self)
        self.timer.setInterval(20) # interval in ms
        self.connect(self.timer, SIGNAL("timeout()"), self.serialPrinter)


        self.timer2 = QTimer(self)
        self.timer2.setInterval(200)
        self.connect(self.timer2,SIGNAL("timeout()"),self.requestStatusService)
        

        self.timer.start()

        

        self.disconnectButton.setEnabled(True)
        self.connectButton.setEnabled(False)

    def test1(self):
        print time.time()


###############################################################################################
###############################################################################################

    def requestStatusService(self):
        while True:
            self.outgoingMessageQ.put("?")
            time.sleep(1)

    
    def messageParserService(self):
        """
        The messageParserService method parses through incoming messages and distributes them
        to the the appropriate widgets

        """

        while True:

            if self.incommingMessageQ.qsize()>0:
                
                #Take a message off the incomming message stack
                incomingMessage = self.incommingMessageQ.get()
                
                if len(incomingMessage) == 0:
                    continue
                

                if incomingMessage[0] == '<':   #Status message
                    messageSplit = incomingMessage.replace('<','').replace('>','').split('|')
                    
                    state = messageSplit[0]
                    mPos = messageSplit[1]
                    FS = messageSplit[2]
                if incomingMessage[0] == '$':   #Settings message
                    pass    

                else:
                    pass

                
                self.serialMonitorQ.put(incomingMessage)




#================================================================================================
#################################################################################################




#================================== grbl commands ================================================
##################################################################################################



    def sendHomeCommand(self):
        self.outgoingMessageQ.put("$H")

    def sendUnlockCommand(self):
        self.outgoingMessageQ.put("$X")


    def createQueues(self):

        self.incommingMessageQ = Queue.Queue()
        self.outgoingMessageQ = Queue.Queue()

        self.serialMonitorQ = Queue.Queue()





    def disconnectFromSerial(self):
        self.ser.close()
        self.serialMonitor.append("Disconnected from serial port")
        self.timer.stop()
        self.connectButton.setEnabled(True)
        self.disconnectButton.setEnabled(False)

    def sendCommand(self):
        cmd = self.sendLineEdit.text()
        print(cmd)
        self.outgoingMessageQ.put(cmd)
        self.sendLineEdit.clear()


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

        #Check boxes
        self.displayAllMessagesCheckBox = QCheckBox('All messages')
        self.okMessagesCheckBox = QCheckBox('Ok Messages')
        self.statusReportsMPosCheckBox = QCheckBox('MPos Messages')
        self.statusReportsWPosCheckBox = QCheckBox('WPos Messages')
        

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
        sideMenuLayout.addWidget(self.okMessagesCheckBox,2,0)
        sideMenuLayout.addWidget(self.statusReportsMPosCheckBox,3,0)
        sideMenuLayout.addWidget(self.statusReportsWPosCheckBox,4,0)
        sideMenuLayout.addWidget(self.displayAllMessagesCheckBox,5,0)
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
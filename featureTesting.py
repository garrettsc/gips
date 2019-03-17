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
        self.createSerialMonitor()
        self.createSideMenu()
        self.createCommandSenderMenu()
        self.SetLayout()


    def messageMonitor(self):
        print('message monitor started')

        lastUpdate = time.time()
        while True:

            #Check if there are messages in the buffer
            if self.ser.in_waiting:
                
                #Read all messages in the buffer
                while self.ser.in_waiting:
                    incomingMessage = self.ser.readline().rstrip()
                    self.incommingMessageQ.put(incomingMessage)

            #Check if there are any outgoing messages            
            if self.outgoingMessageQ.qsize()>0:
                outgoingMessage = self.outgoingMessageQ.get()
                self.ser.write("{}\n".format(outgoingMessage).encode('utf-8'))
                self.incommingMessageQ.put(outgoingMessage)

                #Wait until grbl responds
                while not self.ser.in_waiting:
                    pass
                self.incommingMessageQ.put(self.ser.readline().rstrip())


            else:
                if time.time()-lastUpdate > 1:
                    self.ser.write("?\n".encode('utf-8'))
                    while not self.ser.in_waiting:
                        pass
                    self.incommingMessageQ.put(self.ser.readline().rstrip())
                    


    def mPosMessageParser(self,rawMessage):

        message_split = rawMessage.replace('<','').replace('>','').split('|')
        print message_split



    def mainLoop(self):
 
        if self.incommingMessageQ.qsize() >0:
            while self.incommingMessageQ.qsize()>0:

                #Take the message off the FIFO Queue
                incomingMessage = self.incommingMessageQ.get()

                #Is it a 'ok' confirmation message?
                if incomingMessage =='ok':
                    if self.okMessagesCheckBox.isChecked():
                        self.serialMonitor.append(incomingMessage)
                    continue
                
                #Is it a MPOS Message?
                else:
                    if 'MPos' in incomingMessage and not 'WC' in incomingMessage:
                        if self.statusReportsMPosCheckBox.isChecked():
                            self.serialMonitor.append(incomingMessage)
                            self.mPosMessageParser(incomingMessage)
                        continue
                    elif 'WC' in incomingMessage:
                        if self.statusReportsWPosCheckBox.isChecked():
                            self.serialMonitor.append(incomingMessage)
                        continue
        

    def createSerialMonitor(self):
        self.serialMonitor = QTextEdit()
        self.serialMonitor.setReadOnly(True)

    def connectToSerial(self):
        self.serialMonitor.append("Connecting...")
        self.count = 0

        self.incommingMessageQ = Queue.Queue()
        self.outgoingMessageQ = Queue.Queue()

        self.ser = serial.Serial(
                            port=self.portList.currentText(),
                            baudrate=115200,timeout=1)

        self.serialMonitor.append("connected to"+self.portList.currentText())

        time.sleep(2)

        t = threading.Thread(target=self.messageMonitor)
        t.daemon = True
        t.start()
        self.timer = QTimer(self)
        self.timer.setInterval(20) # interval in ms
        self.connect(self.timer, SIGNAL("timeout()"), self.mainLoop)
        self.timer.start()

        self.disconnectButton.setEnabled(True)
        self.connectButton.setEnabled(False)

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

        #Check boxes
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
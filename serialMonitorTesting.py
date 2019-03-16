from PySide.QtGui import QWidget, QPushButton,QHBoxLayout, QApplication, QGridLayout, QLCDNumber, QLabel, QFrame, QTabWidget, QFont, QTextEdit, QComboBox, QFormLayout, QLineEdit
from PySide.QtCore import QDateTime, QTimer, SIGNAL, QSize, Qt

import sys
import serial.tools.list_ports
import time


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
        self.createMenu()
        self.SetLayout()

    def createSerialMonitor(self):
        self.serialMonitor = QTextEdit()
        self.serialMonitor.setReadOnly(True)

    def connectToSerial(self):
        self.serialMonitor.append("Connecting...")
        self.count = 0

        self.ser = serial.Serial(
                            port=self.portList.currentText(),
                            baudrate=115200,timeout=0.1)

        print("connecting to"+self.portList.currentText())
        self.timer = QTimer(self)
        self.timer.setInterval(20) # interval in ms
        self.connect(self.timer, SIGNAL("timeout()"), self.updateMonitor)
        self.timer.start()

        self.disconnectButton.setEnabled(True)
        self.connectButton.setEnabled(False)

    def disconnectFromSerial(self):
        self.ser.close()
        self.serialMonitor.append("Disconnected from serial port")
        self.timer.stop()
        self.connectButton.setEnabled(True)
        self.disconnectButton.setEnabled(False)


    def updateMonitor(self):
        if self.ser.in_waiting:
            self.serialMonitor.append(self.ser.readline().rstrip())


    def sendCommand(self):
        cmd = self.sendLineEdit.text()
        print(cmd)
        self.ser.write('{}\n'.format(cmd).encode('utf-8'))

        self.sendLineEdit.clear()



    def createMenu(self):
        self.connectButton = QPushButton('Connect')

        self.connectButton.clicked.connect(self.connectToSerial)
        self.disconnectButton = QPushButton('Disconnect')
        self.disconnectButton.clicked.connect(self.disconnectFromSerial)
        self.disconnectButton.setEnabled(False)
        
        self.portList = QComboBox()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.portList.addItem(port.device)


        self.formLayout = QHBoxLayout()
        self.sendLineEdit = QLineEdit()
        self.sendButton = QPushButton("Send")
        self.sendButton.clicked.connect(self.sendCommand)
        self.sendLabel = QLabel("Command:")

        self.formLayout.addWidget(self.sendLabel)
        self.formLayout.addWidget(self.sendLineEdit)
        self.formLayout.addWidget(self.sendButton)

    
    def SetLayout(self):
        gridLayout = QGridLayout()
        
        sideMenuLayout = QGridLayout()

        sideMenuLayout.addWidget(self.connectButton,0,0)
        sideMenuLayout.addWidget(self.disconnectButton,0,1)
        sideMenuLayout.addWidget(self.portList,1,0)

        gridLayout.addWidget(self.serialMonitor,0,0)
        gridLayout.addLayout(sideMenuLayout,0,1)
        gridLayout.addLayout(self.formLayout,1,0)

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
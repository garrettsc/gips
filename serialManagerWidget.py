from PySide.QtGui import QPushButton, QWidget, QApplication, QGridLayout, QSpacerItem, QFrame, QLabel, QGroupBox, QRadioButton, QHBoxLayout, QComboBox
from PySide.QtCore import QTimer

import serial.tools.list_ports
import threading
from messageManager import messageManager

import sys
import time
import zmq
import serial
import Queue


class serialManagerWidget(QGridLayout):
    def __init__(self):
        """
        Name:   messageManager.py

        Description:


        """

        super(serialManagerWidget, self).__init__()


        self.setupSerialManagerButtons()
        self.setupComboBox()
        self.setupLayout()

        self.unQuereiedMessages = Queue.Queue()
        
        self.ser = None



    def setupSerialManagerButtons(self):
        self.connectButton = QPushButton('Connect')
        self.disconnectButton = QPushButton('Disconnect')
        self.connectButton.setEnabled(True)
        self.disconnectButton.setEnabled(False)

        self.connectButton.clicked.connect(self.connectToSerial)
        self.disconnectButton.clicked.connect(self.disconnectFromSerial)



    

    def connectToSerial(self):
        """
        This method attempts to open a serial connection to the selected com port.

        """

        self.ser = serial.Serial(port=self.portList.currentText(),
                                 baudrate=115200,
                                 timeout=1)

        time.sleep(2)

        
        t = threading.Thread(target=messageManager,args=(self.ser,self.unQuereiedMessages))
        t.daemon = True
        t.start()

        port = 5001
        context = zmq.Context()
        self.cmdSocket = context.socket(zmq.REQ)
        self.cmdSocket.connect("tcp://localhost:%s" % port)

        self.connectButton.setEnabled(False)
        self.disconnectButton.setEnabled(True)

    def disconnectFromSerial(self):
        self.ser.close()
        self.connectButton.setEnabled(True)
        self.disconnectButton.setEnabled(False)
    
    def setupComboBox(self):
        self.portList = QComboBox()
        ports = serial.tools.list_ports.comports()[::-1]
        for port in ports:
            self.portList.addItem(port.device)

    
    def setupLayout(self):
        self.serialManagerLayout = QHBoxLayout()
        self.serialManagerLayout.addWidget(self.portList)
        self.serialManagerLayout.addWidget(self.connectButton)
        self.serialManagerLayout.addWidget(self.disconnectButton)
        self.serialManagerBox = QGroupBox('Serial Manager')
        self.serialManagerBox.setLayout(self.serialManagerLayout)
        self.addWidget(self.serialManagerBox,0,0)



class MainWindow(QWidget):
    """ Our Main Window class
    """
    def __init__(self):
        """ Constructor Function
        """

        self.serialManagerPort = 5001

        QWidget.__init__(self)
        self.setWindowTitle("Title")
        self.setGeometry(100, 100, 1000, 300)

        SM = serialManager()

        gridLayout = QGridLayout()
        gridLayout.addLayout(SM,0,0)


        self.setLayout(gridLayout)




if __name__ == '__main__':


    try:
        myApp = QApplication(sys.argv)
        mainWindow = MainWindow()
        mainWindow.show()
        myApp.exec_()

        sys.exit(0)
    except NameError:
        print("Name Error:", sys.exc_info()[1])
    except SystemExit:
        print("Closing Window...")
    except Exception:
        print(sys.exc_info()[1])
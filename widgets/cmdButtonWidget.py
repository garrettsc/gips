from PySide.QtGui import QPushButton, QWidget, QApplication, QGridLayout, QSpacerItem, QFrame, QLabel, QGroupBox, QRadioButton, QVBoxLayout, QFont
from PySide.QtCore import QTimer

import sys
import time
import zmq
import json


class cmdButtonWidget(QGridLayout):
    def __init__(self):
        """
        Name:   

        Description:

        """

        super(cmdButtonWidget, self).__init__()

        self.setupCmdButtonBox()
        self.addGroupBoxes()

        context = zmq.Context()
        port = 5001
        self.cmdButtonSocket = context.socket(zmq.REQ)
        # self.cmdButtonSocket.RCVTIMEO=1000
        self.cmdButtonSocket.connect("tcp://localhost:%s" % port)
        
    def setupCmdButtonBox(self):


        self.homeButton = QPushButton('Home')
        self.unlockButton = QPushButton('Unlock')
        

        #Connect buttons
        self.homeButton.clicked.connect(self.home)
        self.unlockButton.clicked.connect(self.unlock)

        cmdButtonLayout = QGridLayout()

        cmdButtonLayout.addWidget(self.homeButton,0,0)
        cmdButtonLayout.addWidget(self.unlockButton,1,0)        

        self.cmdButtonBox = QGroupBox("GRBL Quick Commands")
        self.cmdButtonBox.setLayout(cmdButtonLayout)


   
    
    def addGroupBoxes(self):
        self.addWidget(self.cmdButtonBox,0,0)


    def home(self):
        self.cmdButtonSocket.send('$H')
        reply = self.cmdButtonSocket.recv()

    def unlock(self):
        self.cmdButtonSocket.send('$X')
        reply = self.cmdButtonSocket.recv()

        
  


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

        jw = cmdButtonWidget()

        gridLayout = QGridLayout()
        gridLayout.addLayout(jw,0,0)


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
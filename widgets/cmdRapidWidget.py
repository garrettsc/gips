from PySide.QtGui import QPushButton, QWidget, QApplication, QGridLayout, QSpacerItem, QFrame, QLabel, QGroupBox, QRadioButton, QVBoxLayout, QFont,QSizePolicy
from PySide.QtCore import QTimer

import sys
import time
import zmq
import json


class cmdRapidWidget(QGridLayout):
    def __init__(self):
        """
        Name:   

        Description:

        """

        super(cmdRapidWidget, self).__init__()

        self.setupRapidButtonBox()
        self.addGroupBoxes()

        context = zmq.Context()
        port = 5001
        self.rapidButtonSocket = context.socket(zmq.REQ)
        self.rapidButtonSocket.connect("tcp://localhost:%s" % port)
        
    def setupRapidButtonBox(self):

        
        self.rapidTwentyFiveButton = QPushButton('25%')
        self.rapidFiftyButton = QPushButton('50%')
        self.rapidOneHundredButton = QPushButton('100%')

        # self.rapidTwentyFiveButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        # self.rapidFiftyButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        # self.rapidOneHundredButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)


    
        #Connect buttons
        self.rapidTwentyFiveButton.clicked.connect(self.rapidTwentyFive)
        self.rapidFiftyButton.clicked.connect(self.rapidFifty)
        self.rapidOneHundredButton.clicked.connect(self.rapidOneHundred)

        


        rapidButtonLayout = QGridLayout()

        rapidButtonLayout.addWidget(self.rapidTwentyFiveButton,0,0)
        rapidButtonLayout.addWidget(self.rapidFiftyButton,0,1)
        rapidButtonLayout.addWidget(self.rapidOneHundredButton,0,2)
     

        self.rapidButtonBox = QGroupBox("Rapid")
        self.rapidButtonBox.setLayout(rapidButtonLayout)


   
    
    def addGroupBoxes(self):
        self.addWidget(self.rapidButtonBox,0,0)

    def rapidTwentyFive(self):

        self.rapidButtonSocket.send('&R25')
        reply = self.rapidButtonSocket.recv()
        print reply

    def rapidFifty(self):

        self.rapidButtonSocket.send('&R50')
        reply = self.rapidButtonSocket.recv()
    
    def rapidOneHundred(self):

        self.rapidButtonSocket.send('&R100')
        reply = self.rapidButtonSocket.recv()
        


    

        
  


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

        jw = cmdRapidWidget()

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
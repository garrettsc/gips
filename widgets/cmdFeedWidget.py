from PySide.QtGui import QPushButton, QWidget, QApplication, QGridLayout, QSpacerItem, QFrame, QLabel, QGroupBox, QRadioButton, QVBoxLayout, QFont,QSizePolicy
from PySide.QtCore import QTimer

import sys
import time
import zmq
import json


class cmdFeedWidget(QGridLayout):
    def __init__(self):
        """
        Name:   

        Description:

        """

        super(cmdFeedWidget, self).__init__()

        self.setupFeedButtonBox()
        self.addGroupBoxes()

        context = zmq.Context()
        port = 5001
        self.feedButtonSocket = context.socket(zmq.REQ)
        # self.feedButtonSocket.RCVTIMEO=1000
        self.feedButtonSocket.connect("tcp://localhost:%s" % port)
        
    def setupFeedButtonBox(self):


        self.feedHoldButton = QPushButton('Feed Hold')

        self.feedHoldButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)


        
        self.feedDownOnePercentButton = QPushButton('-1%')
        self.feedDownTenPercentButton = QPushButton('-10%')
        self.feedOneHundredPercentButton = QPushButton('100%')
        self.feedUpTenPercentButton = QPushButton('+10%')
        self.feedUpOnePercentButton = QPushButton('+1%')

        
        self.feedDownOnePercentButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.feedDownTenPercentButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.feedOneHundredPercentButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.feedUpTenPercentButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.feedUpOnePercentButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)


        
        #Connect buttons
        self.feedHoldButton.clicked.connect(self.feedHold)
        self.feedDownOnePercentButton.clicked.connect(self.feedDecreaseOne)
        self.feedDownTenPercentButton.clicked.connect(self.feedDecreaseTen)
        self.feedOneHundredPercentButton.clicked.connect(self.feedOneHundred)
        self.feedUpTenPercentButton.clicked.connect(self.feedIncreaseTen)
        self.feedUpOnePercentButton.clicked.connect(self.feedIncreaseOne)

        feedButtonLayout = QGridLayout()

        feedButtonLayout.addWidget(self.feedHoldButton,0,0,1,5)
        feedButtonLayout.addWidget(self.feedDownOnePercentButton,1,0)
        feedButtonLayout.addWidget(self.feedDownTenPercentButton,1,1)
        feedButtonLayout.addWidget(self.feedOneHundredPercentButton,1,2)
        feedButtonLayout.addWidget(self.feedUpTenPercentButton,1,3)
        feedButtonLayout.addWidget(self.feedUpOnePercentButton,1,4)     

        self.feedButtonBox = QGroupBox("Feed Overide")
        self.feedButtonBox.setLayout(feedButtonLayout)


   
    
    def addGroupBoxes(self):
        self.addWidget(self.feedButtonBox,0,0)

    def feedHold(self):
        self.feedButtonSocket.send('?')
        reply = self.feedButtonSocket.recv()
        reply = json.loads(reply)
        state = reply[1].replace('<','').replace('>','').split('|')[0]
        
        if state == 'Run':

            self.feedButtonSocket.send('!')
            reply = self.feedButtonSocket.recv()
        
        elif 'Hold' in state:
            self.feedButtonSocket.send('~')
            reply = self.feedButtonSocket.recv()
            print reply

    def feedDecreaseOne(self):
        self.feedButtonSocket.send('&FM01')
        reply = self.feedButtonSocket.recv()

    def feedDecreaseTen(self):
        self.feedButtonSocket.send('&FM10')
        reply = self.feedButtonSocket.recv()

    def feedOneHundred(self):
        self.feedButtonSocket.send('&F100')
        reply = self.feedButtonSocket.recv()

    def feedIncreaseTen(self):
        self.feedButtonSocket.send('&FP10')
        reply = self.feedButtonSocket.recv()

    def feedIncreaseOne(self):
        self.feedButtonSocket.send('&FP01')
        reply = self.feedButtonSocket.recv()

    

        
  


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

        jw = cmdFeedWidget()

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
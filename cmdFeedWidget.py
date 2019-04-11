from PySide.QtGui import QPushButton, QWidget, QApplication, QGridLayout, QSpacerItem, QFrame, QLabel, QGroupBox, QRadioButton, QVBoxLayout, QFont
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
        
        self.feedDownOnePercentButton = QPushButton('-1%')
        self.feedDownTenPercentButton = QPushButton('-10%')
        self.feedOneHundredPercentButton = QPushButton('100%')
        self.feedUpTenPercentButton = QPushButton('+10%')
        self.feedUpOnePercentButton = QPushButton('+1%')

        
# hexList = {'&JOGCANCEL':0x85,
#            '&FO':0x91,
#            '&SD':0x84,              #Safety Door
#            '&F100':0x90,            #Feed 100%
#            '&FP10':0x91,            #Increase Feed 10%
#            '&FM10':0x92,            #Decrease Feed 10%
#            '&FP01':0x93,            #Increase Feed 1%
#            '&FM01':0x94,            #Decrease Feed 1%
#            '&R100':0x95,            #Rapid 100%
#            '&R50' :0x96,            #Rapid 50%
#            '&R25' :0x97,            #Rapid 25%
#            '&S100':0x99,            #Spindle 100%
#            '&SP10':0x9A,            #Increase Spindle 10%
#            '&SM10':0x9B,            #Decrease Spindle 10%
#            '&SP01':0x9C,            #Increase Spindle 1%
#            '&SM01':0x9D,            #Decrease Spindle 1%
#            '&S00' :0x9E,            #Toggle Spindle Stop
#            '&TFC' :0xA0,            #Toggle Flood Coolant
#            '&TMC' :0xA1}            #Toggle Mist Coolant  

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
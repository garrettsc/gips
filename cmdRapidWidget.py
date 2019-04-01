from PySide.QtGui import QPushButton, QWidget, QApplication, QGridLayout, QSpacerItem, QFrame, QLabel, QGroupBox, QRadioButton, QVBoxLayout, QFont
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

        self.feedHoldButton = QPushButton('Feed Hold')
        
        self.rapidTwentyFiveButton = QPushButton('25%')
        self.rapidFiftyButton = QPushButton('50%')
        self.rapidOneHundredButton = QPushButton('100%')


        
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

        self.feedButtonSocket.send('&R25')
        reply = self.feedButtonSocket.recv()

    def rapidFifty(self):

        self.feedButtonSocket.send('&R50')
        reply = self.feedButtonSocket.recv()
    
    def rapidOneHundred(self):

        self.feedButtonSocket.send('&R100')
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
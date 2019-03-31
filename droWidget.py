from PySide.QtGui import QPushButton, QWidget, QApplication, QGridLayout, QSpacerItem, QFrame, QLabel, QGroupBox, QRadioButton, QVBoxLayout
from PySide.QtCore import QTimer

import sys
import time
import zmq


class droWidget(QGridLayout):
    def __init__(self):
        """
        Name:   

        Description:

        """

        super(droWidget, self).__init__()

        context = zmq.Context()
        port = 5001
        self.jogSocket = context.socket(zmq.REQ)
        self.jogSocket.RCVTIMEO=1000
        self.jogSocket.connect("tcp://localhost:%s" % port)

        self.jogCancelSocket = context.socket(zmq.REQ)
        self.jogCancelSocket.connect("tcp://localhost:%s" % port)

        self.setupJogButtonBox()
        self.setupFeedBox()
        self.addGroupBoxes()

    def setupDroBox(self):

       

        self.jogButtonGroupBox = QGroupBox("Manual Jog")
        self.jogButtonGroupBox.setLayout(jogButtonLayout)



    def setupFeedBox(self):

        
        self.feedRadioGroupBox = QGroupBox('Feed Rate')
        self.feedRadioGroupBox.setLayout(self.feedLayout)

    
    
    def addGroupBoxes(self):
        self.addWidget(self.jogButtonGroupBox,0,0)
        self.addWidget(self.feedRadioGroupBox,0,1)


        
  


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

        jw = jogWidget()
        jw2 = jogWidget()

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
        print(sys.exc_info()[1])from PySide.QtGui import QPushButton, QWidget, QApplication, QGridLayout, QSpacerItem, QFrame, QLabel, QGroupBox, QRadioButton, QVBoxLayout
from PySide.QtCore import QTimer

import sys
import time
import zmq


class jogWidget(QGridLayout):
    def __init__(self):
        """
        Name:   jogWidget.py

        Description:

                Custom widget that contains X,Y, and Z Jog buttons
                and feed rate options. 

        """

        super(jogWidget, self).__init__()

        # Feed rate list
        self.feedRates = [100,500,1000,1500,2000]

        # Button Sizes
        widthHeight = 35
        self.jogButtonWidth = widthHeight
        self.jogButtonHeight = widthHeight

        context = zmq.Context()
        port = 5001
        self.jogSocket = context.socket(zmq.REQ)
        self.jogSocket.RCVTIMEO=1000
        self.jogSocket.connect("tcp://localhost:%s" % port)

        self.jogCancelSocket = context.socket(zmq.REQ)
        self.jogCancelSocket.connect("tcp://localhost:%s" % port)

        self.setupJogButtonBox()
        self.setupFeedBox()
        self.addGroupBoxes()

    def setupJogButtonBox(self):

        # Create Buttons
        self.pXJogButton = QPushButton()
        self.nXJogButton = QPushButton()

        self.pYJogButton = QPushButton()
        self.nYJogButton = QPushButton()

        self.pZJogButton = QPushButton()
        self.nZJogButton = QPushButton()

        # Set button labels        
        self.pXJogButton.setText('X+')
        self.nXJogButton.setText('X-')

        self.pYJogButton.setText('Y+')
        self.nYJogButton.setText('Y-')

        self.pZJogButton.setText('Z+')
        self.nZJogButton.setText('z-')

        # Set button functionality when pressed
        self.pXJogButton.pressed.connect(lambda : self.onPress(1,0,0))
        self.nXJogButton.pressed.connect(lambda : self.onPress(-1,0,0))

        self.pYJogButton.pressed.connect(lambda : self.onPress(0,1,0))
        self.nYJogButton.pressed.connect(lambda : self.onPress(0,-1,0))

        self.pZJogButton.pressed.connect(lambda : self.onPress(0,0,1))
        self.nZJogButton.pressed.connect(lambda : self.onPress(0,0,-1))

        # Set button functionality when released
        self.pXJogButton.released.connect(self.onRelease)
        self.nXJogButton.released.connect(self.onRelease)

        self.pYJogButton.released.connect(self.onRelease)
        self.nYJogButton.released.connect(self.onRelease)

        self.pZJogButton.released.connect(self.onRelease)
        self.nZJogButton.released.connect(self.onRelease)

        # Set jog button sizes
        self.pXJogButton.setFixedSize(self.jogButtonWidth,self.jogButtonHeight)
        self.nXJogButton.setFixedSize(self.jogButtonWidth,self.jogButtonHeight)

        self.pYJogButton.setFixedSize(self.jogButtonWidth,self.jogButtonHeight)
        self.nYJogButton.setFixedSize(self.jogButtonWidth,self.jogButtonHeight)

        self.pZJogButton.setFixedSize(self.jogButtonWidth,self.jogButtonHeight)
        self.nZJogButton.setFixedSize(self.jogButtonWidth,self.jogButtonHeight)

        # Add jog buttons to the jog button layout
        jogButtonLayout = QGridLayout()
        jogButtonLayout.addWidget(self.pXJogButton,1,2)
        jogButtonLayout.addWidget(self.nXJogButton,1,0)

        jogButtonLayout.addWidget(self.pYJogButton,0,1)
        jogButtonLayout.addWidget(self.nYJogButton,2,1)

        jogButtonLayout.addWidget(self.pZJogButton,0,4)
        jogButtonLayout.addWidget(self.nZJogButton,2,4)

        # Set minimum width of column 3 to separate XY and Z jog buttons
        jogButtonLayout.setColumnMinimumWidth(3,self.jogButtonWidth)

        self.jogButtonGroupBox = QGroupBox("Manual Jog")
        self.jogButtonGroupBox.setLayout(jogButtonLayout)



    def setupFeedBox(self):

        self.feedLayout = QVBoxLayout()
        
        self.feedRateRadioButtons = []
        for feed in self.feedRates:

            feedRateTitle = '{}'.format(feed)
            
            _feedRateRadio = QRadioButton(feedRateTitle)
            self.feedLayout.addWidget(_feedRateRadio)
            self.feedRateRadioButtons.append(_feedRateRadio)

        self.feedRadioGroupBox = QGroupBox('Feed Rate')
        self.feedRadioGroupBox.setLayout(self.feedLayout)

    
    def checkFeedRate(self):
        for radio in self.feedRateRadioButtons:
            if radio.isChecked():
                return float(radio.text())

    
    def addGroupBoxes(self):
        self.addWidget(self.jogButtonGroupBox,0,0)
        self.addWidget(self.feedRadioGroupBox,0,1)


        
    def setJogButtonState(self,state=bool):
        
        self.pXJogButton.setEnabled(state)
        self.nXJogButton.setEnabled(state)
        self.pYJogButton.setEnabled(state)
        self.nYJogButton.setEnabled(state)

        self.nXJogButton.repaint()
        self.pXJogButton.repaint()
        self.nYJogButton.repaint()
        self.pYJogButton.repaint()

    
    def onPress(self,x=0,y=0,z=0):
        feed = self.checkFeedRate()
        stepSize = 0.1

        self.jogTimer = QTimer()
        self.jogTimer.setInterval(25)
        self.jogTimer.timeout.connect(lambda : self.jogSender(x*stepSize,y*stepSize,z*stepSize,feed))
        self.jogTimer.start()

    def jogSender(self,x,y,z,f):
        jogCmd = '$J=G91X{}Y{}Z{}F{}'.format(x,y,z,f)
        print jogCmd
        self.jogSocket.send(jogCmd)
        self.jogSocket.recv()

    def onRelease(self):
        if self.jogTimer.isActive():
            self.jogTimer.stop()
            self.setJogButtonState(False)
            self.jogCancelSocket.send('&JOGCANCEL')
            _ = self.jogCancelSocket.recv()
            self.setJogButtonState(True)

        
    
    def button1Pushed(self):
        self.setJogButtonState(False)
        time.sleep(5)
        self.setJogButtonState(True)

    def button2Pushed(self):
        print('button2')



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

        jw = jogWidget()
        jw2 = jogWidget()

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
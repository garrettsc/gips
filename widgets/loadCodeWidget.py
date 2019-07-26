from PySide.QtGui import QPushButton, QWidget, QApplication, QGridLayout, QSpacerItem, QFrame, QLabel, QGroupBox, QRadioButton, QVBoxLayout
from PySide.QtCore import QTimer, Signal, SIGNAL

import sys
import time
import zmq


class loadCode(QGridLayout):

    testSignal = Signal(str)

    def __init__(self):

        super(loadCode, self).__init__()


        # Button Sizes
        widthHeight = 65
        self.jogButtonWidth = widthHeight
        self.jogButtonHeight = widthHeight

        context = zmq.Context()
        port = 5001
        self.cmdSocket = context.socket(zmq.REQ)
        # self.cmdSocket.RCVTIMEO=1000
        self.cmdSocket.connect("tcp://localhost:%s" % port)

        self.setupJogButtonBox()
        self.addGroupBoxes()


    def setupWidgets(self):
        pass

        #Recently opened file list
        #Load recently opened file

        #Load file
        

  
    
    def addGroupBoxes(self):
        self.addWidget(self.jogButtonGroupBox,0,0)
        self.addWidget(self.feedRadioGroupBox,0,1)

    

    # def jogSender(self,x,y,z,f):
    #     jogCmd = '$J=G91X{}Y{}Z{}F{}'.format(x,y,z,f)
    #     # print jogCmd
    #     self.jogSocket.send(jogCmd)
    #     self.jogSocket.recv()

    #     # self.testSignal.emit(jogCmd)
    #     # self.emit(SIGNAL("testSignal(str)"), str(jogCmd))

    #     self.testSignal.emit(jogCmd)
        
    



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

        jw = loadCode()

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
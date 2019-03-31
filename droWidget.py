from PySide.QtGui import QPushButton, QWidget, QApplication, QGridLayout, QSpacerItem, QFrame, QLabel, QGroupBox, QRadioButton, QVBoxLayout, QFont
from PySide.QtCore import QTimer

import sys
import time
import zmq
import json


class droWidget(QGridLayout):
    def __init__(self,serialObject = object):
        """
        Name:   

        Description:

        """

        super(droWidget, self).__init__()

        self.droTimer = QTimer()
        self.droTimer.setInterval(100)
        self.droTimer.timeout.connect(self.requestStatusService)
        


        self.setupDroBox()
        self.addGroupBoxes()

    def startDro(self):
        context = zmq.Context()
        port = 5001
        self.statusSocket = context.socket(zmq.REQ)
        self.statusSocket.RCVTIMEO=1000
        self.statusSocket.connect("tcp://localhost:%s" % port)

        self.droTimer.start()
        


    def setupDroBox(self):

        self.droTextWidget = QLabel()
        self.droFormat = "X    {:9.4f}\nY    {:9.4f}\nZ    {:9.4f}"
        self.droTextWidget.setText(self.droFormat.format(0,0,0))
        font = QFont()
        font.setPointSize(15)
        self.droTextWidget.setFont(font)

        droLayout = QVBoxLayout()
        droLayout.addWidget(self.droTextWidget)

        self.droBox = QGroupBox("DRO")
        self.droBox.setLayout(droLayout)


    def requestStatusService(self):
        """
        When called send a '?' status update query across the cmd socket and wait for a response.
        Parse out the status and the machine position from the status. Method needs cleaned up significantly
        """

        try:
            self.statusSocket.send('?')   
            response = self.statusSocket.recv()
        except:
            print ('exception')
            return
        resp = json.loads(response)

        # if 'Ov:' in resp[0]:
        #     self.serialMonitor.append(resp[0])

        data = resp[0].encode('utf-8')
        status =  data.replace('<','').replace('>','').split('|')[0]
        MPos = data.replace('<','').replace('>','').split('|')[1].split(':')[1].split(',')

        self.droTextWidget.setText(self.droFormat.format(float(MPos[0]),float(MPos[1]),float(MPos[2])))
        # self.currentStatusWidget.setText(status)

    
    def addGroupBoxes(self):
        self.addWidget(self.droBox,0,0)
        # self.addWidget(self.feedRadioGroupBox,0,1)


        
  


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

        jw = droWidget()

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
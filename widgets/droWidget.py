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
        
        self.currentStatusDict = {'Status':None,
                                  'WPos:' :None,
                                  'Bf'    :None,
                                  'FS'    :None,
                                  'MPos'  :None}


        self.setupDroBox()
        self.addGroupBoxes()

    def startDro(self):
        context = zmq.Context()
        port = 5001
        self.statusSocket = context.socket(zmq.REQ)
        # self.statusSocket.RCVTIMEO=1000
        self.statusSocket.connect("tcp://localhost:%s" % port)

        self.droTimer.start()
        


    def setupDroBox(self):
        font = QFont()
        font.setPointSize(15)
        font.setBold(True)

        self.droTextWidget = QLabel()
        self.statusWidget = QLabel()

        self.statusWidget.setFrameStyle(QFrame.Panel | QFrame.Raised)



        self.droFormat = "X    {:9.4f}\nY    {:9.4f}\nZ    {:9.4f}"
        # self.droFormat = "<font size=5>X    {:9.4f}<br/><font size=1>{:9.2f}"
        self.droTextWidget.setText(self.droFormat.format(0,0,0))

        self.droTextWidget.setFont(font)
        self.statusWidget.setFont(font)

        droLayout = QVBoxLayout()
        droLayout.addWidget(self.statusWidget)
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

        try:
            messageEncoded = resp[1].encode('utf-8').strip()

            messageSplit = messageEncoded.replace('<','').replace('>','').split('|')

            status = messageSplit[0]
            self.currentStatusDict['Status'] = status
            for message in messageSplit[1:]:
                messageName, messageContents = message.split(':')
                self.currentStatusDict[messageName] = messageContents.split(',')
                # print self.currentStatusDict


            #Update the 'Status' label widget
            # pLabel->setStyleSheet("QLabel { background-color : red; color : blue; }");
            self.updateStatusWidget(self.currentStatusDict['Status'])
            self.statusWidget.setText(self.currentStatusDict['Status'])

            #Update the Digital Read Out widget
            self.droTextWidget.setText(self.droFormat.format(float(self.currentStatusDict['WPos'][0]),
                                                             float(self.currentStatusDict['WPos'][1]),
                                                             float(self.currentStatusDict['WPos'][2])))

        except IndexError as e:
            pass

    def updateStatusWidget(self,status):
        if 'Alarm' in status:
            self.statusWidget.setStyleSheet("QLabel {background-color : red}")
        if 'Idle' in status:
            self.statusWidget.setStyleSheet("QLabel {background-color : grey}")
        if 'Run' in status:
            self.statusWidget.setStyleSheet("QLabel {background-color : green}")
        
        if 'Hold' in status:
            self.statusWidget.setStyleSheet("QLabel {background-color : yellow}")

        if 'Jog' in status:
            self.statusWidget.setStyleSheet("QLabel {background-color : blue}")

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
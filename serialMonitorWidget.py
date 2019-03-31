from PySide.QtGui import QPushButton, QWidget, QApplication, QGridLayout, QSpacerItem, QFrame, QLabel, QGroupBox, QRadioButton, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit
from PySide.QtCore import QTimer

import sys
import time
import zmq
import json


class serialMonitorWidget(QGridLayout):
    def __init__(self,unqueriedMessageQueue):
        """
        Name:   serialMonitorWidget.py

        Description:

        """

        super(serialMonitorWidget, self).__init__()

        self.unqueriedMessageQueue = unqueriedMessageQueue
        
        context = zmq.Context()
        port = 5001
        self.cmdSocket = context.socket(zmq.REQ)
        # self.cmdSocket.RCVTIMEO=1000
        self.cmdSocket.connect("tcp://localhost:%s" % port)

        self.serialMonitorTimer = QTimer()
        self.serialMonitorTimer.setInterval(200)
        self.serialMonitorTimer.timeout.connect(self.checkUnqueriedMessages)
        
        self.setupSerialMonitorWidgets()
        self.addGroupBoxes()

    
    def checkUnqueriedMessages(self):
        if self.unqueriedMessageQueue.qsize() > 0:
            # print self.unqueriedMessageQueue.get()
            self.serialMonitor.append(self.unqueriedMessageQueue.get())



    def startSerialMonitor(self):
        pass


    def sendCommand(self):
        cmd = self.sendLineEdit.text()
        
        self.serialMonitor.append("USER# "+ cmd)
        self.sendLineEdit.clear()
        self.cmdSocket.send_unicode(cmd)
        reply = self.cmdSocket.recv()

        replyList = json.loads(reply)
        print replyList
        if replyList[0] == None:
            pass
            # self.serialMonitor.append(replyList[1])
        else:
            try:
                fullReplyString = ''.join(replyList)
            except IndexError as e:
                self.serialMonitor.append(replyList)
                return

            except TypeError as e:
                return

            self.serialMonitor.append(fullReplyString)


    def setupSerialMonitorWidgets(self):

        self.serialMonitor = QTextEdit()
        self.serialMonitor.setReadOnly(True)
        self.sendLineEdit = QLineEdit()
        self.sendButton = QPushButton("Send")
        self.sendButton.clicked.connect(self.sendCommand)
        self.sendLabel = QLabel("Command:")

        self.commandSendLayout = QHBoxLayout()
        self.commandSendLayout.addWidget(self.sendLabel)
        self.commandSendLayout.addWidget(self.sendLineEdit)
        self.commandSendLayout.addWidget(self.sendButton)


        self.serialMonitorLayout = QVBoxLayout()

        self.serialMonitorLayout.addWidget(self.serialMonitor)
        self.serialMonitorLayout.addLayout(self.commandSendLayout)

        self.serialMonitorGroupBox = QGroupBox("Serial Monitor")
        self.serialMonitorGroupBox.setLayout(self.serialMonitorLayout)


    
    def addGroupBoxes(self):
        self.addWidget(self.serialMonitorGroupBox,0,0)
        

    

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

        jw = serialMonitorWidget()

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
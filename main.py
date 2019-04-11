from PySide.QtGui import QWidget, QPushButton,QHBoxLayout, QApplication, QGridLayout, QLCDNumber, QLabel, QFrame, QTabWidget, QFont, QTextEdit, QComboBox, QFormLayout, QLineEdit, QCheckBox, QIcon
from PySide.QtCore import QDateTime, QTimer, SIGNAL, QSize, Qt

import zmq

import sys
import serial.tools.list_ports
import time
import threading
import Queue
import json
from messageManager import messageManager
from jogWidget import jogWidget
from serialManagerWidget import serialManagerWidget
from messageManager import *
from serialMonitorWidget import serialMonitorWidget
from droWidget import droWidget
from cmdButtonWidget import cmdButtonWidget
from cmdFeedWidget import cmdFeedWidget
from cmdRapidWidget import cmdRapidWidget
from settingsWidget import *

class MainWindow(QWidget):
    """ Our Main Window class
    """
    def __init__(self):
        """ Constructor Function
        """

        self.serialManagerPort = 5001

        QWidget.__init__(self)
        self.setWindowTitle("grbl Serial Monitor")
        self.setGeometry(100, 100, 1000, 300)
        appIcon = QIcon('icon.png')
        self.setWindowIcon(appIcon)

         
    def launch(self):
        """
        This method sets up widgets, layouts, and any other at-runtime services
        """
        self.SetLayout()
        self.setTimers()
        self.checkConnectionTimer.start()




    def SetLayout(self):
        gridLayout = QGridLayout()

        self.jogWidget = jogWidget()
        self.SMW = serialManagerWidget()
        self.serMon = serialMonitorWidget(self.SMW.unQuereiedMessages)
        self.serMon.serialMonitorTimer.start()
        self.dro = droWidget()
        self.quickCmdWidget = cmdButtonWidget()
        self.feedCmdWidget = cmdFeedWidget()
        self.cmdRapidWidget = cmdRapidWidget()
        
        self.settingsWidget = settingsWidget()

        gridLayout.addLayout(self.SMW,0,0)
        gridLayout.addLayout(self.jogWidget,1,0)
        gridLayout.addLayout(self.serMon,2,0,2,2)
        gridLayout.addLayout(self.dro,1,1)
        gridLayout.addLayout(self.quickCmdWidget,0,1)
        gridLayout.addLayout(self.feedCmdWidget,4,0)
        gridLayout.addLayout(self.cmdRapidWidget,4,2)

        gridLayout.addLayout(self.settingsWidget,0,2,4,3)


        self.setLayout(gridLayout)


        

    def setTimers(self):
        self.checkConnectionTimer = QTimer()
        self.checkConnectionTimer.setInterval(1000)
        print('timers created')
        self.checkConnectionTimer.timeout.connect(self.checkIfConnected)
        print('connected')
        self.droTimer = QTimer()
        
    
    def checkIfConnected(self):
        # print('checking if connected...')
        if not self.SMW.ser == None:
            if self.SMW.ser.is_open:
                # print ('Is Connected')
                if not self.dro.droTimer.isActive():
                    self.dro.startDro()
            else:
                if self.dro.droTimer.isActive():
                    self.dro.droTimer.stop()



if __name__ == '__main__':
    # Exception Handling
    try:
        QApplication.setStyle('plastique')
        myApp = QApplication(sys.argv)
        mainWindow = MainWindow()

        mainWindow.launch()

        mainWindow.show()
        myApp.exec_()
        sys.exit(0)
    except NameError:
        print("Name Error:", sys.exc_info()[1])
    except SystemExit:
        print("Closing Window...")
    except Exception:
        print(sys.exc_info()[1])
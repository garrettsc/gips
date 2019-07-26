from PySide.QtGui import QWidget, QPushButton,QHBoxLayout, QApplication, QGridLayout, QLCDNumber, QLabel, QFrame, QTabWidget, QFont, QTextEdit, QComboBox, QFormLayout, QLineEdit, QCheckBox, QIcon
from PySide.QtCore import QDateTime, QTimer, SIGNAL, QSize, Qt

import zmq

import sys
import serial.tools.list_ports
import time
import threading
import Queue
import json
from widgets.messageManager import messageManager
from widgets.jogWidget import jogWidget
from widgets.serialManagerWidget import serialManagerWidget
from widgets.messageManager import *
from widgets.serialMonitorWidget import serialMonitorWidget
from widgets.droWidget import droWidget
from widgets.cmdButtonWidget import cmdButtonWidget
from widgets.cmdFeedWidget import cmdFeedWidget
from widgets.cmdRapidWidget import cmdRapidWidget
from widgets.settingsWidget import *
from widgets.streamGcodeWidget import streamGcodeWidget
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

        self.dynamicDisplayWidget = QTextEdit()

        self.streamWidget = streamGcodeWidget()


        self.manualControlLayout = QGridLayout()
        self.manualControlLayout.addLayout(self.jogWidget,0,0,2,2)
        self.manualControlLayout.addLayout(self.feedCmdWidget,0,3)
        self.manualControlLayout.addLayout(self.cmdRapidWidget,1,3)
        
        self.manualControlWidget = QWidget()
        self.manualControlWidget.setLayout(self.manualControlLayout)

        self.serialMonitorWidget = QWidget()
        self.serialMonitorWidget.setLayout(self.serMon)

        self.settingsTabWidget = QWidget()
        self.settingsTabWidget.setLayout(self.settingsWidget)

        self.runProgramWidget = QLabel('Place gcode loading widget here')

        self.tab = QTabWidget()
        self.tab.addTab(self.manualControlWidget,'Manual')
        self.tab.addTab(self.runProgramWidget,'Run Program')
        self.tab.addTab(self.serialMonitorWidget,'Serial Monitor')
        self.tab.addTab(self.settingsTabWidget,'GRBL Settings')

        self.tab.setStyleSheet("QTabBar::tab { height: 25px; width: 150px}")

        self.tab.setEnabled(False)

        gridLayout.addLayout(self.SMW,0,0,1,2)

        gridLayout.addLayout(self.dro,1,0)
        gridLayout.addLayout(self.quickCmdWidget,1,1)

        
        gridLayout.addWidget(self.tab,5,0,1,6)
        gridLayout.addLayout(self.settingsWidget,0,2,4,3)

        gridLayout.addLayout(self.streamWidget,0,2,3,1)

        self.setLayout(gridLayout)



    def connectWidgets(self):
        self.jogWidget.testSignal.connect(self.serMon.testingSIGNALS)

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
                
                if not self.jogWidget.buttonStates:
                    self.jogWidget.setButtonStates(True)
                    self.tab.setEnabled(True)

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
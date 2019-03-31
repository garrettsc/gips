from PySide.QtGui import QWidget, QPushButton,QHBoxLayout, QApplication, QGridLayout, QLCDNumber, QLabel, QFrame, QTabWidget, QFont, QTextEdit, QComboBox, QFormLayout, QLineEdit, QCheckBox
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
from serialMonitorWidget import serialMonitorWidget

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

         
    def launch(self):
        """
        This method sets up widgets, layouts, and any other at-runtime services
        """
        self.SetLayout()




    def SetLayout(self):
        gridLayout = QGridLayout()
        

        


        self.jogWidget = jogWidget()
        self.SMW = serialManagerWidget()
        self.serMon = serialMonitorWidget()
        

       


        gridLayout.addLayout(self.SMW,0,0)
        gridLayout.addLayout(self.jogWidget,1,0)
        gridLayout.addLayout(self.serMon,2,0,1,2)


        self.setLayout(gridLayout)


if __name__ == '__main__':
    # Exception Handling
    try:
        #QApplication.setStyle('plastique')
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
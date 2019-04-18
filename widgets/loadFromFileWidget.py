from PySide.QtGui import QPushButton, QWidget, QApplication, QGridLayout, QSpacerItem, QFrame, QLabel, QGroupBox, QRadioButton, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QListWidget, QListWidgetItem, QFileDialog
from PySide.QtCore import QTimer
from PySide.QtCore import QTranslator as tr

import sys
import time
import zmq
import json

# fileName = QFileDialog.getOpenFileName(self,
#     tr("Open Image"), "/home/jana", tr("Image Files (*.png *.jpg *.bmp)"))

class loadFromFileWidget(QGridLayout):
    def __init__(self):
        """
        Name:   serialMonitorWidget.py

        Description:

        """

        super(loadFromFileWidget, self).__init__()

        
        context = zmq.Context()
        port = 5001
        self.cmdSocket = context.socket(zmq.REQ)
        self.cmdSocket.connect("tcp://localhost:%s" % port)


        
        self.setupLoadFromFileWidgets()
        # self.addGroupBoxes()

    
    def setupLoadFromFileWidgets(self):

        self.loadFromFileButton = QPushButton('Load File')
        self.loadFromFileButton.clicked.connect(self.loadFromFile)
        self.listWidget = QListWidget()
        

        items = ['one','two','three']
        for row,item in enumerate(items):
            newItem = QListWidgetItem()
            newItem.setText(item)
            self.listWidget.insertItem(row, newItem)



        # self.layout = QGridLayout()

        self.recentFilesGroupBox = QGroupBox('Recently Loaded Files')
        self.recentFilesGroupBox.setLayout()

        self.addWidget(self.listWidget,0,0)
        self.addWidget(self.loadFromFileButton,0,1)

        # self.serialMonitor = QTextEdit()
        # self.serialMonitor.setReadOnly(True)
        # self.sendLineEdit = QLineEdit()
        # self.sendButton = QPushButton("Send")
        # self.sendButton.clicked.connect(self.sendCommand)
        # self.sendLabel = QLabel("Command:")

        # self.commandSendLayout = QHBoxLayout()
        # self.commandSendLayout.addWidget(self.sendLabel)
        # self.commandSendLayout.addWidget(self.sendLineEdit)
        # self.commandSendLayout.addWidget(self.sendButton)


        # self.serialMonitorLayout = QVBoxLayout()

        # self.serialMonitorLayout.addWidget(self.serialMonitor)
        # self.serialMonitorLayout.addLayout(self.commandSendLayout)

        # self.serialMonitorGroupBox = QGroupBox("Serial Monitor")
        # self.serialMonitorGroupBox.setLayout(self.serialMonitorLayout)


    
    def addGroupBoxes(self):
        self.addWidget(self.serialMonitorGroupBox,0,0)


    def loadFromFile(self):

        ITEM = self.listWidget.currentItem()
        self.listWidget.openPersistentEditor(ITEM)
        

    

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

        jw = loadFromFileWidget()

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
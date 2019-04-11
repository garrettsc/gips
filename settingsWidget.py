from PySide.QtGui import QPushButton, QWidget, QApplication, QGridLayout, QSpacerItem, QFrame, QLabel, QGroupBox, QRadioButton, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QTableView
from PySide.QtCore import QTimer, QAbstractTableModel
from PySide.QtCore import *

import sys
import time
import zmq
import json


class settingsWidget(QGridLayout):
    def __init__(self):
        """
        Name:   serialMonitorWidget.py

        Description:

        """

        super(settingsWidget, self).__init__()

       
        
        context = zmq.Context()
        port = 5001
        self.cmdSocket = context.socket(zmq.REQ)
        self.cmdSocket.connect("tcp://localhost:%s" % port)
        
        self.setupWidgets()
        self.addGroupBoxes()

    

    def setupWidgets(self):

        header = ['$ #','Setting']
        self.tableModel = TableModel(self,[('1','2')],header)
        self.tableView = QTableView()
        self.tableView.setModel(self.tableModel)



        self.tableLayout = QHBoxLayout()
        self.tableLayout.addWidget(self.tableView)

        self.loadSettingsGrblButton = QPushButton('Load from GRBL')
        self.loadSettingsFile = QPushButton('Load from File')
        self.writeSettingsToGrbl = QPushButton('Write Settings')
        self.saveSettingsToFile = QPushButton('Save to File')

        self.loadSettingsGrblButton.clicked.connect(self.getSettingsFromGrbl)

        self.settingsButtonLayout = QGridLayout()
        self.settingsButtonLayout.addWidget(self.loadSettingsGrblButton,0,0)
        self.settingsButtonLayout.addWidget(self.loadSettingsFile,0,1)
        self.settingsButtonLayout.addWidget(self.writeSettingsToGrbl,1,0)
        self.settingsButtonLayout.addWidget(self.saveSettingsToFile,1,1)


        self.settingsLayout = QGridLayout()
        self.settingsLayout.addWidget(self.tableView,0,0)
        self.settingsLayout.addLayout(self.settingsButtonLayout,0,1)

        # self.serialMonitorLayout.addWidget(self.serialMonitor)
        # self.serialMonitorLayout.addLayout(self.commandSendLayout)

        self.tableGroupBox = QGroupBox("Serial Monitor")
        self.tableGroupBox.setLayout(self.settingsLayout)



    
    def addGroupBoxes(self):
        self.addWidget(self.tableGroupBox,0,0)


    
    def getSettingsFromGrbl(self):

        self.cmdSocket.send('$$')
        reply = self.cmdSocket.recv()
        settings=json.loads(reply)[1].replace('ok','')

        settingsList = settings.split('\n')[:-1]
        
        settingLabel = [val.split('=')[0] for val in settingsList]
        settingValue = [val.split('=')[1] for val in settingsList]

        
        # self.tableModel.mylist = zip(settingLabel,settingValue)

        header = ['$ #','Setting']
        self.tableModel = TableModel(self,zip(settingLabel,settingValue),header)
        self.tableView.setModel(self.tableModel)
        
        

        # return zip(settingLabel,settingValue)

        

class TableModel(QAbstractTableModel):

    def __init__(self,parent,mylist,header,*args):
        QAbstractTableModel.__init__(self,parent,*args)

        self.mylist = mylist
        self.header = header
    
    def rowCount(self,parent):
        return len(self.mylist)
    
    def columnCount(self,parent):
        return len(self.mylist[0])

    def data(self,index,role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return self.mylist[index.row()][index.column()]

    def headerData(self,col,orientation,role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]


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

        jw = settingsWidget()

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
from PySide.QtGui import QPushButton, QWidget, QApplication, QGridLayout, QSpacerItem, QFrame, QLabel, QGroupBox, QRadioButton, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QTableView,QTableWidgetItem,QHeaderView
from PySide.QtCore import QTimer, QAbstractTableModel
from PySide.QtCore import *

import sys
import time
import zmq
import json
import os
import datetime

class settingsWidget(QGridLayout):
    def __init__(self):
        """
        Name:   serialMonitorWidget.py

        Description:

        """

        super(settingsWidget, self).__init__()

        self.settingsSavePath = os.path.join(os.getcwd(),'saves')
        
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
        self.tableView.horizontalHeader().setResizeMode(QHeaderView.Stretch)

        self.tableView.setShowGrid(False)

        self.tableLayout = QHBoxLayout()
        self.tableLayout.addWidget(self.tableView)

        self.loadSettingsGrblButton = QPushButton('Load from GRBL')
        self.loadSettingsFile = QPushButton('Load from File')
        self.writeSettingsToGrblButton = QPushButton('Write Settings to GRBL')
        self.writeSettingsToFileButton = QPushButton('Save to File')

        self.writeSettingsToGrblButton.setEnabled(False)
        self.writeSettingsToFileButton.setEnabled(False)

        self.loadSettingsGrblButton.clicked.connect(self.getSettingsFromGrbl)
        self.writeSettingsToGrblButton.clicked.connect(self.writeSettingsToGrbl)
        self.writeSettingsToFileButton.clicked.connect(self.writeSettingsToFile)

        self.settingsButtonLayout = QGridLayout()
        self.settingsButtonLayout.addWidget(self.loadSettingsGrblButton,0,0)
        self.settingsButtonLayout.addWidget(self.loadSettingsFile,1,0)
        self.settingsButtonLayout.addWidget(self.writeSettingsToGrblButton,2,0)
        self.settingsButtonLayout.addWidget(self.writeSettingsToFileButton,3,0)


        self.settingsLayout = QGridLayout()
        self.settingsLayout.addWidget(self.tableView,0,0)
        self.settingsLayout.addLayout(self.settingsButtonLayout,0,1)


    
    def addGroupBoxes(self):
        self.addLayout(self.settingsLayout,0,0)


    def writeSettingsToFile(self):

        settings_ffp = os.path.join(self.settingsSavePath, datetime.datetime.now().strftime('grblSettings_%Y-%m-%d_%H:%M:%S.txt'))
        with open(settings_ffp,'w+') as fWrite:
            for line in self.tableModel.mylist:
                lineToWrite = ",".join([line[0],line[2]])+"\n"
                fWrite.write(lineToWrite)

    def readSettingDescriptionsFromFile(self):

        pathToSettingsFile = os.path.join(os.getcwd(),'csv','setting_codes_en_US.csv')
        self.settingsDescriptions = []
        with open(pathToSettingsFile,'r') as fRead:
            for idx,line in enumerate(fRead):
                if idx > 0:
                    lsplit = line.replace('"','').split(',')
                    self.settingsDescriptions.append(lsplit[1:])

    def writeSettingsToGrbl(self):
        """ Read current values in settings table and write them to grbl"""
        
        for setting in self.tableModel.mylist:
            settingId = setting[0]
            settingValue = setting[2]
            settingMessage = '{}={}'.format(settingId,settingValue)

            self.cmdSocket.send(settingMessage)
            reply = self.cmdSocket.recv()
        
    
    def getSettingsFromGrbl(self):
        """ 
        Request current settings from grbl, parse the results,
        and them to the tables abstract model for display.
        """

        # Request settings from grbl
        self.cmdSocket.send('$$')
        reply = self.cmdSocket.recv()

        reply = json.loads(reply)
        
        # If the reply is in error or alarm state, cancel
        if reply[0] != 0:
            print 'error'
            return
        
        # Unpack the settings message and remove the 'ok' status
        settings=reply[1].replace('ok','')

        # Split message based on newline character
        settingsList = settings.split('\n')[:-1]
        
        settingLabel = [val.split('=')[0] for val in settingsList]
        settingValue = [val.split('=')[1] for val in settingsList]

        self.readSettingDescriptionsFromFile()

        settingDescriptions = [line[0] for line in self.settingsDescriptions]
        header = ['$ #','Description','Value']

        grblSettings = [[settingLabel[idx],settingDescriptions[idx],settingValue[idx]] for idx in range(0,len(settingLabel))]
        self.tableModel = TableModel(self,grblSettings,header)
        self.tableView.setModel(self.tableModel)

        for idx in range(0,len(grblSettings)):
            self.tableView.setRowHeight(idx,14)

        self.writeSettingsToGrblButton.setEnabled(True)
        self.writeSettingsToFileButton.setEnabled(True)

        

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


    def flags(self, index):

        if not index.isValid():
            return Qt.ItemIsEnabled
        
        if not index.column() == 2:
            return Qt.ItemIsEnabled
            
        return Qt.ItemFlags(QAbstractTableModel.flags(self, index) | Qt.ItemIsEditable)

    def setData(self, index, value, role):
        
        if not index.isValid():
            return False
        
        if role != Qt.EditRole:
            return False

        row = index.row()
        if row < 0 or row >= len(self.mylist):
            return False
        
        column = index.column()
        if column < 0 or column >= len(self.header):
            return False

        if column != 2:
            return False

        try:
            updatedValue = int(value)
        except:
            return False

        self.mylist[row][column] = updatedValue
        self.dataChanged.emit(index,index)
        return True
     


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
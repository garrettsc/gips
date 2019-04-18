from PySide.QtGui import QPushButton, QWidget, QApplication, QGridLayout, QSpacerItem, QFrame, QLabel, QGroupBox, QRadioButton, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QListWidget, QListWidgetItem, QFileDialog, QTextCursor, QTableView
from PySide.QtCore import QTimer, QAbstractTableModel
from PySide.QtCore import *
from PySide.QtGui import *

import sys
import time
import zmq
import json
import time

class streamGcodeWidget(QGridLayout):
    def __init__(self):
        """
        Name:   serialMonitorWidget.py

        Description:

        """

        super(streamGcodeWidget, self).__init__()

        
        context = zmq.Context()
        port = 5001
        self.cmdSocket = context.socket(zmq.REQ)
        self.cmdSocket.connect("tcp://localhost:%s" % port)

        self.idx = 0
        
        self.setupLoadFromFileWidgets()

    
    def setupLoadFromFileWidgets(self):

        self.loadFromFileButton = QPushButton('Load File')
        self.nextLineButton = QPushButton('Next Line')
        self.nextLineButton.setEnabled(False)
        self.loadFromFileButton.clicked.connect(self.loadFromFile)
        self.nextLineButton.clicked.connect(self.next)
        self.gcodeStreamingBox = QTextEdit()
        self.gcodeStreamingBox.setReadOnly(True)

        self.tableView = QTableView()
        self.tableView.setShowGrid(False)

        

        self.addWidget(self.tableView,0,0)
        self.addWidget(self.loadFromFileButton,0,1)
        self.addWidget(self.nextLineButton,1,1)
    
    def buildTable(self):

        self.tableModel = TableModel(self,self.program,['g-code','status'])
        self.tableView.setModel(self.tableModel)
        for idx in range(0,len(self.program)):
            self.tableView.setRowHeight(idx,14)

        header = self.tableView.horizontalHeader()

        header.setResizeMode(0, QHeaderView.Stretch)
        header.setResizeMode(1, QHeaderView.ResizeToContents)
        header.setResizeMode(2, QHeaderView.ResizeToContents)



    def next(self):
        print 'here'
        self.tableModel.mylist[self.idx][1] = 'ok'
        self.tableModel.mylist[self.idx+1][1] = 'Staged'
        self.idx+=1
        
        self.tableModel.dataChanged.emit(self.idx,1)
        
        try:
            self.tableView.selectRow(self.idx+5)
        except:
            pass
        self.tableView.selectRow(self.idx)

    


    def loadFromFile(self):

        exampleGcode_ffp = '/home/garrett/projects/gips/gcode/example2.nc'

        self.program = []
        with open(exampleGcode_ffp,'r') as fRead:
            for line in fRead:
                self.program.append([line,''])
        
        self.nextLineButton.setEnabled(True)
        self.buildTable()
        
        
        
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

        if role == Qt.BackgroundRole:
            if index.column() == 1:
                if self.mylist[index.row()][index.column()] =='ok':
                    return QBrush(Qt.green)

        elif role == Qt.TextAlignmentRole:
            return Qt.AlignVCenter

        elif role != Qt.DisplayRole:
            return None
        return self.mylist[index.row()][index.column()]

    def headerData(self,col,orientation,role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]


    def flags(self, index):

        if not index.isValid():
            return Qt.ItemIsEnabled
            
        return Qt.ItemFlags(QAbstractTableModel.flags(self, index) | Qt.ItemIsSelectable)

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
        self.setGeometry(100, 100, 500, 300)

        jw = streamGcodeWidget()

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
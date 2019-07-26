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
                
        self.currentStatusDict = {'Status':None,
                                  'WPos:' :None,
                                  'Bf'    :None,
                                  'FS'    :None,
                                  'MPos'  :None}
        
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
        self.nextLineButton.clicked.connect(self.onPress)
        self.gcodeStreamingBox = QTextEdit()
        self.gcodeStreamingBox.setReadOnly(True)

        self.tableView = QTableView()
        self.tableView.setShowGrid(False)

        
        self.addWidget(self.tableView,0,0,2,1)
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


    def onPress(self):
        self.checkConnectionTimer = QTimer()
        self.checkConnectionTimer.setInterval(10)
        self.checkConnectionTimer.timeout.connect(self.sendLine)
        self.checkConnectionTimer.start()

    def sendLine(self):
        self.requestStatusService()
        print self.currentStatusDict['Bf']
        if not int(self.currentStatusDict['Bf'][0]) < 10:
            cmdToSend = self.tableModel.mylist[self.idx][0]
            self.cmdSocket.send(cmdToSend)
            reply = self.cmdSocket.recv()
            self.tableModel.mylist[self.idx][1] = 'ok'
            self.tableModel.mylist[self.idx+1][1] = 'Staged'
            self.idx+=1
            
            self.tableModel.dataChanged.emit(self.idx,1)
            
            try:
                self.tableView.selectRow(self.idx+5)
            except:
                pass
            self.tableView.selectRow(self.idx)
        else:
            pass


    def requestStatusService(self):
        """
        When called send a '?' status update query across the cmd socket and wait for a response.
        Parse out the status and the machine position from the status. Method needs cleaned up significantly
        """

        try:
            self.cmdSocket.send('?')
            response = self.cmdSocket.recv()

        except:
            print ('exception')
            return
        resp = json.loads(response)

        try:
            messageEncoded = resp[1].encode('utf-8').strip()

            messageSplit = messageEncoded.replace('<','').replace('>','').split('|')

            status = messageSplit[0]
            self.currentStatusDict['Status'] = status
            for message in messageSplit[1:]:
                messageName, messageContents = message.split(':')
                self.currentStatusDict[messageName] = messageContents.split(',')


            #Update the 'Status' label widget
            # pLabel->setStyleSheet("QLabel { background-color : red; color : blue; }");
            # self.updateStatusWidget(self.currentStatusDict['Status'])
            # self.statusWidget.setText(self.currentStatusDict['Status'])

            # #Update the Digital Read Out widget
            # self.droTextWidget.setText(self.droFormat.format(float(self.currentStatusDict['WPos'][0]),
            #                                                  float(self.currentStatusDict['WPos'][1]),
            #                                                  float(self.currentStatusDict['WPos'][2])))

        except IndexError as e:
            pass
    


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
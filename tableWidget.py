
from PySide.QtCore import QAbstractTableModel
from PySide.QtGui import QTableView, QGridLayout

from PySide.QtCore import *
from PySide.QtGui import *

import sys
import numpy as np




class settingsTableWidet(QGridLayout):

    def __init__(self,data,header,*args):

        super(settingsTableWidet,self).__init__()

        data = self.loadFromCSV()
        header = data[0]
        tableModel = myTableModel(self,data[1:],header)
        tableView = QTableView()
        tableView.setModel(tableModel)


        tableView.resizeColumnsToContents()

        self.addWidget(tableView)

    def loadFromCSV(self):

        path = '/home/garrett/projects/gips/csv/setting_codes_en_US.csv'

        settings = []
        with open(path,'r') as fRead:
            for line in fRead:
                settings.append(tuple(line.replace('"','').split(',')))

        return settings

        

        


class myTableModel(QAbstractTableModel):

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
        elif role !=Qt.DisplayRole:
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

        header = ['Parameter','Value']
        dataList = [('$1','one'),('$2','two','$3','three')]

        QWidget.__init__(self)
        self.setWindowTitle("Title")
        self.setGeometry(100, 100, 1000, 300)

        stw = settingsTableWidet(dataList,header)

        gridLayout = QGridLayout()
        gridLayout.addLayout(stw,0,0)


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
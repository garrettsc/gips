from PySide.QtGui import QWidget, QPushButton,QHBoxLayout, QApplication, QGridLayout, QLCDNumber, QLabel, QFrame, QTabWidget, QFont, QTextEdit
from PySide.QtCore import QDateTime, QTimer, SIGNAL, QSize, Qt

import sys



class MainWindow(QWidget):
    """ Our Main Window class
    """
    def __init__(self):
        """ Constructor Function
        """
        QWidget.__init__(self)
        self.setWindowTitle("Horizontal Layout")
        self.setGeometry(100, 100, 1000, 600)

    
    def launch(self):
        self.createReadOut()
        self.createLabels()
        self.createSerialMonitor()
        self.setupMenu()
        

        self.SetLayout()



    def createReadOut(self):
        self.droStyle = "QLabel {font:bold 30px}"
        self.droTextAlignment = Qt.AlignLeft

        self.droTextFormat = '{:>15}'
        font = QFont()
        font.setPointSize(10)

        self.droTextWidget = QLabel()
        n = 25
        self.droTextWidget.setText("X    "+"+1.2345" \
                                    +"\nY     "+"-1.2345"\
                                    +"\nZ    "+"+1.2345")
        self.droTextWidget.setFont(font)
        self.droTextWidget.setStyleSheet(self.droStyle)
        self.droTextWidget.setAlignment(self.droTextAlignment)
        self.droTextWidget.setFrameStyle(QFrame.Sunken | QFrame.Panel | QFrame.Box)


    def createSerialMonitor(self):
        self.serialMonitor = QTextEdit()



    def setupMenu(self):

        self.manualTabLabel = QLabel()
        self.manualTabLabel.setText("This is the manual menu.")
        self.manualTabLabel.setFrameStyle(QFrame.Sunken | QFrame.Panel)

        self.setupTabLabel = QLabel()
        self.setupTabLabel.setText("This is the steup menu")
        self.setupTabLabel.setFrameStyle(QFrame.Sunken | QFrame.Panel)


        self.tab = QTabWidget()
        self.tab.addTab(self.manualTabLabel,'Manual')
        self.tab.addTab(self.setupTabLabel,'Setup')
        self.tab.addTab(self.serialMonitor,'Serial Monitor')
        self.tab.setStyleSheet("QTabBar::tab { height: 50px; width: 100px}")



    def createLabels(self):

        font = QFont()
        font.setPointSize(10)

        
        self.label2 = QLabel()
        self.label2.setText("Label2")
        self.label2.setFrameStyle(QFrame.Sunken | QFrame.Panel)

        self.label3 = QLabel()
        self.label3.setText("Label3")
        self.label3.setFrameStyle(QFrame.Sunken | QFrame.Panel)

        self.label4 = QLabel()
        self.label4.setText("Label4")
        self.label4.setFrameStyle(QFrame.Sunken | QFrame.Panel)

        self.label1a = QLabel()
        self.label1a.setText("Label1a")
        self.label1a.setFont(font)
        self.label1a.setFrameStyle(QFrame.Sunken | QFrame.Panel)

        self.label1b = QLabel()
        # self.label1b.setText(self.droTextFormat.format(123.456))
        self.label1b.setText("X"+"1.2345".rjust(10))

        self.label1b.setFont(font)
        self.label1b.setStyleSheet(self.droStyle)
        self.label1b.setAlignment(self.droTextAlignment)
        self.label1b.setFrameStyle(QFrame.Sunken | QFrame.Panel | QFrame.Box)


        self.label1c = QLabel()
        self.label1c.setText("Label1c")
        self.label1c.setFont(font)
        self.label1c.setFrameStyle(QFrame.Sunken | QFrame.Panel)

        self.labelInTab1 = QLabel()
        self.labelInTab1.setText("LabelInTab1")
        self.labelInTab1.setFrameStyle(QFrame.Sunken | QFrame.Panel)

        self.labelInTab2 = QLabel()
        self.labelInTab2.setText("LabelInTab2")
        self.labelInTab2.setFrameStyle(QFrame.Sunken | QFrame.Panel)

        
        
        


    
    def SetLayout(self):



        gridLayout = QGridLayout()
        subGridLayout = QGridLayout()

        # subGridLayout.addWidget(self.myTimeDisplay,0,0)
        # subGridLayout.addWidget(self.label1b,1,0)
        # subGridLayout.addWidget(self.label1c,2,0)


        gridLayout.addWidget(self.droTextWidget,0,0)
        gridLayout.setRowMinimumHeight(0,200)
        gridLayout.setRowMinimumHeight(2,200)

        gridLayout.addWidget(self.label2,0,1,1,2)
        gridLayout.addWidget(self.tab,2,0,1,3)
        self.setLayout(gridLayout)






if __name__ == '__main__':
    # Exception Handling
    try:
        #QApplication.setStyle('plastique')
        myApp = QApplication(sys.argv)
        mainWindow = MainWindow()
        # mainWindow.createReadOut()
        # mainWindow.createLabels()

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
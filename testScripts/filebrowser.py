from PySide import QtCore,QtGui

def do_file():
    fname = QtGui.QFileDialog.getOpenFileName()
    print fname

app = QtGui.QApplication([])

button = QtGui.QPushButton("Test File")
button.clicked.connect(do_file)
button.show()

app.exec_()
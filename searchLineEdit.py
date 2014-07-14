from PyQt4 import QtCore, QtGui

class SearchLineEdit(QtGui.QLineEdit):
    upKeyPressed = QtCore.pyqtSignal()
    downKeyPressed = QtCore.pyqtSignal()
    def __init__(self, *args):
        QtGui.QLineEdit.__init__(self, *args)
    
    def keyPressEvent(self, key_event):
        if (key_event.key() == QtCore.Qt.Key_Up):
            self.upKeyPressed.emit()
        elif(key_event.key() == QtCore.Qt.Key_Down):
            self.downKeyPressed.emit()
        else:
            return QtGui.QLineEdit.keyPressEvent(self, key_event)
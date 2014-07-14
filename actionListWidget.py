from PyQt4 import QtCore, QtGui

class ActionListWidget(QtGui.QListWidget):
    returnKeyPressed = QtCore.pyqtSignal()
    
    def __init__(self, *args):
        QtGui.QListWidget.__init__(self, *args)
    
    def keyPressEvent(self, key_event):
        if ((key_event.key() == QtCore.Qt.Key_Return) or (key_event.key() == QtCore.Qt.Key_Enter)):
            self.returnKeyPressed.emit()
        else:
            return QtGui.QListWidget.keyPressEvent(self, key_event)
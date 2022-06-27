from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot

class ActionListWidget(QtWidgets.QListWidget):
    returnKeyPressed = QtCore.pyqtSignal()
    itemEditRequested = QtCore.pyqtSignal(str)
    def __init__(self, *args):
        QtWidgets.QListWidget.__init__(self, *args)
    def keyPressEvent(self, key_event):
        if ((key_event.key() == QtCore.Qt.Key_Return) or (key_event.key() == QtCore.Qt.Key_Enter)):
            self.returnKeyPressed.emit()
        else:
            return QtWidgets.QListWidget.keyPressEvent(self, key_event)
            
    def contextMenuEvent(self, context_menu_event):
        self.list_item_right_clicked(context_menu_event.globalPos())
        
    def select_next_action(self):
        if (self.currentRow() < (self.count() - 1)):
            self.setCurrentRow(self.currentRow() + 1)
        
    def select_previous_action(self):
        if (self.currentRow() > 0):
            self.setCurrentRow(self.currentRow() - 1)
            
    def list_item_right_clicked(self, pos):
        itemMenu = QtWidgets.QMenu()

        menu_item = itemMenu.addAction("Edit...")
        menu_item.triggered.connect(self.edit_item)
        itemMenu.exec_(pos)
    
    @pyqtSlot()
    def edit_item(self):
        self.itemEditRequested.emit(str(self.currentItem().text()))
        

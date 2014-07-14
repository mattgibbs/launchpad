from PyQt4 import QtCore, QtGui
from actionDetailDialog_ui import Ui_actionDetailDialog

class ActionDetailDialog(QtGui.QDialog):
    Deleted = 666 #custom result code signaling a request to delete the action.
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_actionDetailDialog()
        self.ui.setupUi(self)
        self.ui.deleteButton.clicked.connect(self.return_delete_result_code)
        
    def show_with_action(self,action):
        self.setWindowTitle("Edit " + '"' + action["name"] + '"')
        self.ui.nameEdit.setText(action["name"])
        self.ui.commandEdit.setText(action["command"])
        return self.exec_()
        
    def return_delete_result_code(self):
        self.done(self.Deleted)
        
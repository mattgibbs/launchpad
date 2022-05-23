from PyQt5 import QtWidgets, uic
import os

class ActionDetailDialog(QtWidgets.QDialog):
    Deleted = 666 #custom result code signaling a request to delete the action.
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi(os.path.join(os.path.dirname(os.path.abspath(__file__)), "actionDetailDialog.ui"), self)
        self.ui.deleteButton.clicked.connect(self.return_delete_result_code)
        
    def show_with_action(self,action):
        self.setWindowTitle("Edit " + '"' + action["name"] + '"')
        self.ui.nameEdit.setText(action["name"])
        self.ui.commandEdit.setText(action["command"])
        if action["window_title_regex"] is not None:
            self.ui.regexEdit.setText(action["window_title_regex"])
        return self.exec_()
        
    def show_for_new_action(self):
        self.setWindowTitle("Add new action")
        self.ui.deleteButton.hide()
        return self.exec_()
        
    def return_delete_result_code(self):
        self.done(self.Deleted)
        
    def accept(self):
        if ((len(str(self.ui.nameEdit.text())) > 0) and (len(str(self.ui.commandEdit.text())) > 0)):
            return QtWidgets.QDialog.accept(self)
        else:
            return QtWidgets.QDialog.reject(self)

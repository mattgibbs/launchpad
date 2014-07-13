import sys
import sqlite3
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSlot
from launchpad_ui import Ui_launchpadDialog

class Launchpad(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_launchpadDialog()
        self.ui.setupUi(self)
        self.initialize_sqlite()
        self.list_all_actions()
        self.connect_slots()
        
    def initialize_sqlite(self):
        self.conn = sqlite3.connect('launchpad.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='actions'")
        if self.cursor.fetchone() == None:
            print("No sqlite database detected, populating a new one.")
            #The actions table doesn't exist!  Go ahead and make one.
            self.cursor.execute("CREATE TABLE actions (name text, command text, launchcount integer)")
            actions = [('Big Red Unlatch', 'edm -x -noscrl $EDM/misc/giantUnlatchAll.edl', 0),
                       ('Steering Panel', 'edm -x $EDM/misc/integratedSteeringPanel.edl', 0),
                       ('Energy Loss Scan', 'xterm -T "FEL E-Loss Scan xterm" -e MatlabGUI E_loss_scan', 0),
                       ('Strip Tool', 'StripTool', 0),
                       ('Emittance Scans', 'xterm -T "Emittance GUI xterm" -e MatlabGUI emittance_gui', 0),
                       ('Beta Matching', 'xterm -T "Matching GUI xterm" -e MatlabGUI matching_gui', 0)]
            self.cursor.executemany('INSERT INTO actions VALUES (?,?,?)', actions)
            self.conn.commit()
            
    def connect_slots(self):
        self.ui.actionListWidget.currentItemChanged.connect(self.on_list_item_changed)
        self.ui.searchLineEdit.returnPressed.connect(self.return_pressed)
            
    def list_all_actions(self):
        for action_name in self.cursor.execute("SELECT name FROM actions"):
            self.ui.actionListWidget.addItem(action_name[0])
           
    def on_list_item_changed(self, curr, prev):
        self.currentlySelectedListItem = curr
        print "New item selected."
    
    def return_pressed(self):
        self.launch_selected_action()
    
    def launch_selected_action(self):
        self.cursor.execute("SELECT command FROM actions WHERE name=?", (str(self.currentlySelectedListItem.text()),))
        print(self.cursor.fetchone())
        
            
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = Launchpad()
    myapp.show()
    sys.exit(app.exec_())
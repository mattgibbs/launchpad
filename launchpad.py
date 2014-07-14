import sys
import sqlite3
import operator
from PyQt4 import QtCore, QtGui
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
        self.ui.searchLineEdit.textChanged.connect(self.filter_action_list)
        self.ui.actionListWidget.itemDoubleClicked.connect(self.launch_selected_action) 
        self.ui.actionListWidget.returnKeyPressed.connect(self.launch_selected_action)
        self.ui.goButton.clicked.connect(self.launch_selected_action)   
    
    def list_all_actions(self):
        for action_name in self.cursor.execute("SELECT name FROM actions"):
            self.ui.actionListWidget.addItem(action_name[0])
               
    def return_pressed(self):
        self.launch_selected_action()
        
    def launch_selected_action(self):
        selected_item = self.ui.actionListWidget.currentItem()
        if selected_item:
            selected_action_name = str(selected_item.text())
            self.cursor.execute("SELECT command FROM actions WHERE name=?", (selected_action_name,))
            print(self.cursor.fetchone())
    
    def filter_action_list(self):
        self.ui.actionListWidget.clear()
        scores = {}
        for action_row in self.cursor.execute("SELECT name, launchcount FROM actions"):
            scores[action_row[0]] = self.score_for_string_with_search_term(str(action_row[0]), str(self.ui.searchLineEdit.text()), 0)
        sorted_scores = sorted(scores.iteritems(), key=operator.itemgetter(1))
        sorted_scores.reverse()
        for tuple in sorted_scores:
            if tuple[1] > 0:
                self.ui.actionListWidget.addItem(tuple[0])
        self.ui.actionListWidget.setCurrentRow(0)
        
    def score_for_string_with_search_term(self, string_to_search, search_term, offset):
        string_to_search = string_to_search.lower()
        search_term = search_term.lower()

        if (len(search_term) == 0):
            return 0.9
        if (len(search_term) > len(string_to_search)):
            return 0.0

        for i in range(len(search_term),0,-1):
            sub_search = search_term[:i]
            index = string_to_search.find(sub_search)
            if (index >= 0):
                if (index + len(search_term) <= len(string_to_search) + offset):
                    next_string = string_to_search[index+len(sub_search):]
                    next_search = None
                    if (i >= len(search_term)):
                        next_search = ""
                    else:
                        next_search = search_term[i:]
                    remaining_score = self.score_for_string_with_search_term(next_string, next_search, offset + index)
                    if (remaining_score > 0):
                        score = len(string_to_search) - len(next_string)
                        if (index != 0):
                            c = string_to_search[index - 1]
                            if (c == ' ') or (c == '\t'):
                                for jj in range((index - 2),0,-1):
                                    cc = string_to_search[jj]
                                    if (cc == ' ') or (cc == '\t'):
                                        score -= 1
                                    else:
                                        score -= 0.15
                            else:
                                score -= index
                        score += remaining_score * len(next_string)
                        score = score / len(string_to_search)
                        return score
        return 0
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = Launchpad()
    myapp.show()
    sys.exit(app.exec_())
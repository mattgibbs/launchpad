import os
import sys
import sqlite3
import operator
import subprocess
from PyQt5 import QtCore, QtWidgets, uic
from actionDetailDialog import ActionDetailDialog
import wmctrl

class Launchpad(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi(os.path.join(os.path.dirname(os.path.abspath(__file__)), "launchpad.ui"), self)
        self.initialize_sqlite()
        self.filter_action_list()
        self.connect_slots()
        
    def initialize_sqlite(self):
        self.conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)),'launchpad.db'))
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='actions'")
        if self.cursor.fetchone() == None:
            print("No sqlite database detected, populating a new one.")
            #The actions table doesn't exist!  Go ahead and make one.
            self.cursor.execute("CREATE TABLE actions (name text, command text, launchcount integer, window_title_regex text)")
            actions = [('Big Red Unlatch', 'edm -x -noscrl $EDM/misc/giantUnlatchAll.edl', 0, 'Big Red Unlatch'),
                       ('Steering Panel', 'edm -x $EDM/misc/integratedSteeringPanel.edl', 0, 'Integrated Steering Panel'),
                       ('Energy Loss Scan', 'xterm -T "FEL E-Loss Scan xterm" -e MatlabGUI E_loss_scan', 0, 'E_loss_scan'),
                       ('Strip Tool', 'StripTool', 0, '.+\.stp Graph'),
                       ('Emittance Scans', 'xterm -T "Emittance GUI xterm" -e MatlabGUI emittance_gui', 0, 'Emittance Application - /[.+/]'),
                       ('Beta Matching', 'xterm -T "Matching GUI xterm" -e MatlabGUI matching_gui', 0, 'matching_gui')]
            self.cursor.executemany('INSERT INTO actions VALUES (?,?,?,?)', actions)
            self.conn.commit()
        self.upgrade_db()
    
    def connect_slots(self):
        self.ui.searchLineEdit.textChanged.connect(self.filter_action_list)
        self.ui.searchLineEdit.upKeyPressed.connect(self.ui.actionListWidget.select_previous_action)
        self.ui.searchLineEdit.downKeyPressed.connect(self.ui.actionListWidget.select_next_action)
        self.ui.actionListWidget.itemDoubleClicked.connect(self.launch_selected_action) 
        self.ui.actionListWidget.returnKeyPressed.connect(self.launch_selected_action)
        self.ui.actionListWidget.itemEditRequested.connect(self.show_edit_dialog_for_item)
        self.ui.goButton.clicked.connect(self.launch_selected_action)
        self.ui.addButton.clicked.connect(self.show_new_action_dialog)
    
    def list_all_actions(self):
        for action_name in self.cursor.execute("SELECT name FROM actions"):
            self.ui.actionListWidget.addItem(action_name[0])
               
    def return_pressed(self):
        self.launch_selected_action()
    
    def launch_selected_action(self):
        selected_item = self.ui.actionListWidget.currentItem()
        if selected_item:
            selected_action_name = str(selected_item.text())
            action = self.get_action_with_name(selected_action_name)
            #Check if there is an open window for this action, if so, just activate it.
            if action["window_title_regex"] is not None and len(action["window_title_regex"]) > 0:
                open_windows = wmctrl.Window.by_name(action["window_title_regex"].encode('utf-8'))
                if len(open_windows) > 0:
                    # First sort the windows in a way that puts windows on your current desktop on the top of the list.
            # This is a pretty slow way to sort but it should be fine unless we have hundreds of windows with the same name.
                    current_desktop = wmctrl.current_desktop()
                    open_windows.sort(key=lambda window: abs(current_desktop - window.desktop))
                    # We just pick the first window in the list if there are multiple windows.  This is somewhat random.
                    open_windows[0].activate()
                    self.update_launch_count(action["name"], action["launchcount"]+1)
                    QtWidgets.QApplication.instance().exit()
                    return
            #print("Running command: " + action["command"])
            process = subprocess.Popen(action["command"], shell=True)
            self.update_launch_count(action["name"], action["launchcount"]+1)
        self.ui.searchLineEdit.setText("")
        QtWidgets.QApplication.instance().exit()
    
    def show_new_action_dialog(self):
        newDialog = ActionDetailDialog(self)
        result = newDialog.show_for_new_action()
        if (result == newDialog.Accepted):
            new_name = str(newDialog.ui.nameEdit.text())
            new_command = str(newDialog.ui.commandEdit.text())
            new_regex = str(newDialog.ui.regexEdit.text())
            self.add_new_action(new_name, new_command, new_regex)
        
    def show_edit_dialog_for_item(self, item_name):
        action = self.get_action_with_name(item_name)
        editDialog = ActionDetailDialog(self)
        result = editDialog.show_with_action(action)
        if (result == editDialog.Accepted):
            #Save the changes to the action.
            edited_name = str(editDialog.ui.nameEdit.text())
            edited_command = str(editDialog.ui.commandEdit.text())
            edited_regex = str(editDialog.ui.regexEdit.text())
            self.update_action(item_name,edited_name,edited_command,edited_regex)
        elif (result == editDialog.Deleted):
            #Delete the action.
            self.delete_action(item_name)
    
    def filter_action_list(self):
        self.ui.actionListWidget.clear()
        scores = {}
        for action_row in self.cursor.execute("SELECT name, launchcount FROM actions"):
            scores[action_row[0]] = self.score_for_string_with_search_term(str(action_row[0]), str(self.ui.searchLineEdit.text()), 0)
        sorted_scores = sorted(scores.items(), key=operator.itemgetter(1))
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
    
    def activateWindow(self):
    #Sadly, wmctrl is the only way to absolutely, positively give your window focus and bring it to the front.
        subprocess.Popen("wmctrl -x -R Launchpad", shell=True)
        super(Launchpad, self).activateWindow()
    
    def get_action_with_name(self, action_name):
        self.cursor.execute("SELECT name, command, launchcount, window_title_regex FROM actions WHERE name=?",(str(action_name),))
        action_row = self.cursor.fetchone()
        return {"name": str(action_row[0]), "command": str(action_row[1]), "launchcount": action_row[2], "window_title_regex": action_row[3]}
        
    def add_new_action(self, new_name, new_command, new_window_title_regex=''):
        self.cursor.execute("INSERT INTO actions (name, command, launchcount, window_title_regex) VALUES (?,?,0,?)", (str(new_name), str(new_command), str(new_window_title_regex),))
        self.conn.commit()
        self.filter_action_list()
    
    def update_action(self, action_name, new_name, new_command, new_window_title_regex=''):
        self.cursor.execute("UPDATE actions SET name=?,command=?,window_title_regex=? WHERE name=?", (str(new_name),str(new_command),str(new_window_title_regex), str(action_name),))
        self.conn.commit()
        self.filter_action_list()
    
    def update_launch_count(self, action_name, new_launch_count):
        self.cursor.execute("UPDATE actions SET launchcount=? WHERE name=?", (str(new_launch_count), str(action_name),))
        self.conn.commit()
    
    def delete_action(self, action_name):
        self.cursor.execute("DELETE FROM actions WHERE name=?", (str(action_name),))
        self.conn.commit()
        self.filter_action_list()
        
    def upgrade_db(self):
        self.cursor.execute("SELECT * FROM actions")
        col_names = [desc[0] for desc in self.cursor.description]
        if 'window_title_regex' not in col_names:
            self.cursor.execute("ALTER TABLE actions ADD COLUMN 'window_title_regex' 'text'")
            self.conn.commit()

if __name__ == "__main__":
    unique_id = "launchpadapp"
    app = QtWidgets.QApplication(sys.argv)
    window = Launchpad()
    window.show()
    sys.exit(app.exec_())

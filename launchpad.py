import sys
from PyQt4 import QtCore, QtGui
from launchpad_ui import Ui_launchpadDialog

class Launchpad(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_launchpadDialog()
        self.ui.setupUi(self)
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = Launchpad()
    myapp.show()
    sys.exit(app.exec_())
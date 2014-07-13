# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'launchpad.ui'
#
# Created: Sun Jul 13 02:45:38 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_launchpadDialog(object):
    def setupUi(self, launchpadDialog):
        launchpadDialog.setObjectName(_fromUtf8("launchpadDialog"))
        launchpadDialog.resize(450, 240)
        self.searchLineEdit = QtGui.QLineEdit(launchpadDialog)
        self.searchLineEdit.setGeometry(QtCore.QRect(30, 30, 341, 21))
        self.searchLineEdit.setObjectName(_fromUtf8("searchLineEdit"))
        self.actionListWidget = QtGui.QListWidget(launchpadDialog)
        self.actionListWidget.setGeometry(QtCore.QRect(30, 70, 341, 141))
        self.actionListWidget.setObjectName(_fromUtf8("actionListWidget"))
        self.addButton = QtGui.QPushButton(launchpadDialog)
        self.addButton.setGeometry(QtCore.QRect(375, 185, 61, 32))
        self.addButton.setAutoDefault(False)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.goButton = QtGui.QPushButton(launchpadDialog)
        self.goButton.setGeometry(QtCore.QRect(375, 25, 61, 32))
        self.goButton.setAutoDefault(False)
        self.goButton.setDefault(True)
        self.goButton.setObjectName(_fromUtf8("goButton"))

        self.retranslateUi(launchpadDialog)
        QtCore.QMetaObject.connectSlotsByName(launchpadDialog)

    def retranslateUi(self, launchpadDialog):
        launchpadDialog.setWindowTitle(_translate("launchpadDialog", "Launchpad", None))
        self.addButton.setText(_translate("launchpadDialog", "+", None))
        self.goButton.setText(_translate("launchpadDialog", "Go", None))


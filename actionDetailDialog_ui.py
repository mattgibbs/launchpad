# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'actionDetailDialog.ui'
#
# Created: Mon Jul 14 02:25:00 2014
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

class Ui_actionDetailDialog(object):
    def setupUi(self, actionDetailDialog):
        actionDetailDialog.setObjectName(_fromUtf8("actionDetailDialog"))
        actionDetailDialog.setWindowModality(QtCore.Qt.NonModal)
        actionDetailDialog.resize(570, 180)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(actionDetailDialog.sizePolicy().hasHeightForWidth())
        actionDetailDialog.setSizePolicy(sizePolicy)
        actionDetailDialog.setModal(True)
        self.verticalLayoutWidget = QtGui.QWidget(actionDetailDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 571, 192))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(20)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.nameFieldLabel = QtGui.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nameFieldLabel.sizePolicy().hasHeightForWidth())
        self.nameFieldLabel.setSizePolicy(sizePolicy)
        self.nameFieldLabel.setObjectName(_fromUtf8("nameFieldLabel"))
        self.verticalLayout.addWidget(self.nameFieldLabel)
        self.nameEdit = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.nameEdit.setObjectName(_fromUtf8("nameEdit"))
        self.verticalLayout.addWidget(self.nameEdit)
        self.commandFieldLabel = QtGui.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.commandFieldLabel.sizePolicy().hasHeightForWidth())
        self.commandFieldLabel.setSizePolicy(sizePolicy)
        self.commandFieldLabel.setObjectName(_fromUtf8("commandFieldLabel"))
        self.verticalLayout.addWidget(self.commandFieldLabel)
        self.commandEdit = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.commandEdit.setObjectName(_fromUtf8("commandEdit"))
        self.verticalLayout.addWidget(self.commandEdit)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.deleteButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.deleteButton.setEnabled(True)
        self.deleteButton.setObjectName(_fromUtf8("deleteButton"))
        self.horizontalLayout.addWidget(self.deleteButton)
        self.buttonBox = QtGui.QDialogButtonBox(self.verticalLayoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(actionDetailDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), actionDetailDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), actionDetailDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(actionDetailDialog)

    def retranslateUi(self, actionDetailDialog):
        actionDetailDialog.setWindowTitle(_translate("actionDetailDialog", "Dialog", None))
        self.nameFieldLabel.setText(_translate("actionDetailDialog", "Action Name:", None))
        self.commandFieldLabel.setText(_translate("actionDetailDialog", "Shell Command:", None))
        self.deleteButton.setText(_translate("actionDetailDialog", "Delete Action", None))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Zoloedov_is\Desktop\py scripts\tabbed\calendar\datetime.ui'
#
# Created: Tue Aug 06 15:22:09 2019
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

class Ui_selectDateTime(object):
    def setupUi(self, selectDateTime):
        selectDateTime.setObjectName(_fromUtf8("selectDateTime"))
        selectDateTime.setWindowModality(QtCore.Qt.WindowModal)
        selectDateTime.resize(341, 144)
        self.okButton = QtGui.QPushButton(selectDateTime)
        self.okButton.setGeometry(QtCore.QRect(70, 100, 75, 23))
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.cancelButton = QtGui.QPushButton(selectDateTime)
        self.cancelButton.setGeometry(QtCore.QRect(190, 100, 75, 23))
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.verticalLayoutWidget = QtGui.QWidget(selectDateTime)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(90, 0, 160, 80))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.dateEdit = QtGui.QDateEdit(self.verticalLayoutWidget)
        self.dateEdit.setDisplayFormat("yyyy-MM-dd")
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setObjectName(_fromUtf8("dateEdit"))
        self.verticalLayout.addWidget(self.dateEdit)
        self.timeEdit = QtGui.QTimeEdit(self.verticalLayoutWidget)
        self.timeEdit.setObjectName(_fromUtf8("timeEdit"))
        self.verticalLayout.addWidget(self.timeEdit)

        self.retranslateUi(selectDateTime)
        QtCore.QMetaObject.connectSlotsByName(selectDateTime)

    def retranslateUi(self, selectDateTime):
        selectDateTime.setWindowTitle(_translate("selectDateTime", "Выбор даты и времени", None))
        self.okButton.setText(_translate("selectDateTime", "Да", None))
        self.cancelButton.setText(_translate("selectDateTime", "Отмена", None))


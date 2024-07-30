# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'report.ui'
#
# Created: Tue Dec 17 13:12:05 2019
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

class Ui_Report_Form(object):
    def setupUi(self, Report_Form):
        Report_Form.setObjectName(_fromUtf8("Report_Form"))
        Report_Form.resize(522, 183)
        Report_Form.setStyleSheet(_fromUtf8("QLabel {background-color: none}"))
        self.label_Title = QtGui.QLabel(Report_Form)
        self.label_Title.setGeometry(QtCore.QRect(60, 20, 411, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_Title.setFont(font)
        self.label_Title.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_Title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Title.setObjectName(_fromUtf8("label_Title"))
        self.label_From = QtGui.QLabel(Report_Form)
        self.label_From.setGeometry(QtCore.QRect(50, 85, 21, 31))
        self.label_From.setObjectName(_fromUtf8("label_From"))
        self.label_To = QtGui.QLabel(Report_Form)
        self.label_To.setGeometry(QtCore.QRect(300, 80, 21, 39))
        self.label_To.setObjectName(_fromUtf8("label_To"))
        self.reportButton_pdf = QtGui.QPushButton(Report_Form)
        self.reportButton_pdf.setGeometry(QtCore.QRect(70, 140, 181, 23))
        self.reportButton_pdf.setObjectName(_fromUtf8("reportButton_pdf"))
        self.fromDateButton = QtGui.QPushButton(Report_Form)
        self.fromDateButton.setGeometry(QtCore.QRect(70, 90, 181, 23))
        self.fromDateButton.setObjectName(_fromUtf8("fromDateButton"))
        self.toDateButton = QtGui.QPushButton(Report_Form)
        self.toDateButton.setGeometry(QtCore.QRect(330, 90, 181, 23))
        self.toDateButton.setObjectName(_fromUtf8("toDateButton"))
        self.reportButton_excel = QtGui.QPushButton(Report_Form)
        self.reportButton_excel.setGeometry(QtCore.QRect(330, 140, 181, 23))
        self.reportButton_excel.setObjectName(_fromUtf8("reportButton_excel"))

        self.retranslateUi(Report_Form)
        QtCore.QMetaObject.connectSlotsByName(Report_Form)

    def retranslateUi(self, Report_Form):
        Report_Form.setWindowTitle(_translate("Report_Form", "Формирование отчёта", None))
        self.label_Title.setText(_translate("Report_Form", "Отчёт по сферическому узлу учёта", None))
        self.label_From.setText(_translate("Report_Form", "С:", None))
        self.label_To.setText(_translate("Report_Form", "По:", None))
        self.reportButton_pdf.setText(_translate("Report_Form", "Сформировать отчёт", None))
        self.fromDateButton.setText(_translate("Report_Form", "Дата начала отчёта", None))
        self.toDateButton.setText(_translate("Report_Form", "Дата окончания отчёта", None))
        self.reportButton_excel.setText(_translate("Report_Form", "Отчёт в Excel", None))


# coding: utf-8
import sys
from PyQt4 import QtGui, QtCore
from tabbed import Tabbed
import mainwindow_ui

class MainWindow(QtGui.QMainWindow, mainwindow_ui.Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.tabbed = Tabbed()
        self.tabbed.worker.qsizeSignal.connect(self.statusbar.showMessage)
        # self.tabbed.reader.start()
        self.setCentralWidget(self.tabbed)
        self.actionStart.triggered.connect(self.tabbed.go)
        self.actionStop.triggered.connect(self.tabbed.stop)
        self.setGeometry(QtCore.QRect(10, 35, 0, 0))
        self.setWindowTitle(u"Теплоучёт")


def main():
    app = QtGui.QApplication(sys.argv)
    icon = QtGui.QIcon()
    icon.addFile("invader.ico", QtCore.QSize(16,16))
    app.setWindowIcon(icon)
    main = MainWindow()
    main.showMaximized()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
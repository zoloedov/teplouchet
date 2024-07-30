# coding: utf-8
# import sqlite3
from PyQt4 import QtCore

class ReportThread(QtCore.QThread):
    def __init__(self, from_to_tab, queue, parent=None):
        super(ReportThread, self).__init__(parent)
        self.running = False
        self.from_to_tab = from_to_tab
        self.queue = queue

    def run(self):
        self.running = True
        self.get_report()
        self.stop()

    def get_report(self):
        pass
        

    def stop(self):
        self.running = False
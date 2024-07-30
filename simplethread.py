# coding: utf-8
from PyQt4 import QtCore

class SimpleThread(QtCore.QThread):
    listSignal = QtCore.pyqtSignal([list, int, str, str, list, dict])#, name = "listSignal")
    def __init__(self):
        super(SimpleThread, self).__init__()
        # self.listSignal = QtCore.pyqtSignal([list], name = "listSignal") # не работает

    def run(self):
        self.running = True
        # self.emit(self.listSignal, [1,23,4,5]) # не работает
        self.listSignal.emit([1,2,3, "affaf", {"a": 2323, "b": 777}],
                            134535677888, "0YLRiyDRhdGD0LkK", "bHVja3kgYmFzdGFyZAo=", [1,2,3], {"a":"a"})

    def stop(self):
        self.running = False


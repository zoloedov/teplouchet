# coding: utf-8
from PyQt4 import QtCore

class Worker(QtCore.QThread):
    qsizeSignal = QtCore.pyqtSignal(str)
    def __init__(self, queue):
        super(Worker, self).__init__()
        self.queue = queue
        self.running = False

    def run(self):
        self.running = True
        while self.isRunning:
            self.qsize = "queue size: %s"%str(self.queue.qsize())
            self.qsizeSignal.emit(self.qsize)
            self.task = self.queue.get()
            self.task.run()
            self.queue.task_done()

# coding: utf-8
import math
import random
import sqlite3
import datetime
# from functools import partial
from PyQt4 import QtCore
from tag_map_dic import new_lineEdits, old_lineEdits, new_TotallineEdits, old_TotallineEdits, sn_lineEdits

lineEdits = {"new_": new_lineEdits, "sn_": sn_lineEdits, "old_": old_lineEdits}

class WriteTask(QtCore.QObject):
    def __init__(self, sql):
        super(WriteTask, self).__init__()
        self.sql = sql

    def run(self):
        self.connection = sqlite3.connect("vkt.db")
        self.cursor = self.connection.cursor()
        # self.cursor.executemany("INSERT INTO vkt_data (name, quality, value, timestamp, test, scheme)\
                             # VALUES (?,?,?,?,?,?); ",self.sql)
        self.cursor.execute(self.sql)
        self.connection.commit()
        self.cursor.close()


class RandomDataThread(QtCore.QThread):
    randomdataSignal = QtCore.pyqtSignal(dict)
    def __init__(self, queue):
        super(RandomDataThread, self).__init__()
        self.running = False
        self.queue = queue

    def run(self):
        self.running = True
        print("started random thread")
        while self.running:
            for scheme, lineEdit in lineEdits.items():
                self.get_random_data(scheme, lineEdit)
                self.randomdataSignal.emit({"lineEdit" : lineEdit, "values" : self.values})
            self.sleep(60)
        print("stopped random thread")

    def stop(self):
        self.running = False
        print "sotp random command"
        # print self.queue.qsize()

    def get_random_data(self, scheme, lineEdit):
        self.values = list()
        self.querys = list()
        for i in range(len(lineEdit)):
            self.rand = random.random()*100*math.exp(math.sin(random.random())) - random.random()*10
            self.name = lineEdit[i][9:] #remove lineEdit_ prefix
            self.value = str(i)# str(round(self.rand,2))
            self.values.append(self.value)
            self.quality = random.choice(["Good",# "Error", "Uncertain", "Good", "Good",
                                            "Good", "Good", "Good", "Good", "Good", "Good"])
            self.time = datetime.datetime.now()
            self.scheme = scheme
            self.order = i
            self.values_list = [self.name, self.quality, "None" if self.quality == "Error" else self.value,
                                datetime.datetime.now() if self.time is None else self.time, 1, self.scheme, self.order]

    


            self.query = "INSERT INTO vkt_data (name, quality, value, timestamp, test, scheme, report_order)\
                             VALUES ('%s','%s','%s','%s','%s', '%s', '%s'); "%tuple(self.values_list)
            # self.querys.append(tuple(self.values_list))
            self.write_task = WriteTask(self.query) # self.query
            self.queue.put(self.write_task)


    def get_total(self, values):
        return sum(values)

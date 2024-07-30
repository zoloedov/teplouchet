# coding: utf-8
from datetime import datetime
import sqlite3
import matplotlib.pyplot as plt
import numpy as np

lineEdits = [#"lineEdit_NEW_TPK2FlowDirect", "lineEdit_New_TPK2FlowBack",\
             # "lineEdit_New_TPK1FlowDirect", "lineEdit_New_TPK1FlowBack",\
             # "lineEdit_New_400FlowDirect", "lineEdit_New_400FlowBack",\
             "lineEdit_Old_400TvQ",\
             "lineEdit_Old_400FlowDirect", "lineEdit_Old_400FlowBack",\
             # "lineEdit_Old_400TempDirect", "lineEdit_Old_400TempBack",\
             # "lineEdit_Old_400PressureDirect", "lineEdit_Old_400PressureBack",\
             # "lineEdit_New_TPK2FlowDirect", "lineEdit_New_TPK2FlowBack"\
             # "lineEdit_New_400Feed",\
             # "lineEdit_New_Level",\
             # "lineEdit_New_400TvM"\
             ]
connection = sqlite3.connect("vkt.db")
cursor = connection.cursor()
plt.figure("chart")

for edit in lineEdits:
    result = cursor.execute("SELECT value, timestamp FROM vkt_data WHERE name = '%s' AND quality = 'Good';"%edit)
                            # AND timestamp > datetime('now', 'localtime', 'start of day', '+3 hour');"%edit)


    result = result.fetchall()
    values = [float(el[0]) for el in result]
    times = [datetime.strptime(el[1].split(".")[0], "%Y-%m-%d %H:%M:%S") for el in result]
    plt.plot(times, values, label=edit)
cursor.close()

plt.grid(True)
plt.legend()
plt.title(u"Параметры теплосети")
plt.show()
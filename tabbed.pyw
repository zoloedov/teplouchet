# coding: utf-8
import schedule
import time
import sys
import random
import webbrowser
import Queue
from datetime import datetime
from datetime import timedelta
from functools import partial
from PyQt4 import QtGui, QtCore
import tabbed_ui
from report import Report
from randomdatathread import RandomDataThread
from opcthread import OpcThread
from reportthread import ReportThread
from workerthread import Worker
from readtask import PDFTask, ExcelTask
from tag_map_dic import new_lineEdits, old_lineEdits, new_TotallineEdits, old_TotallineEdits, sn_lineEdits

lineEdits = {"new_": new_lineEdits, "sn_": sn_lineEdits, "old_": old_lineEdits}

BAK_IMAGE_HEIGHT = 272 # 281
BAK_HEIGHT = 12

queue = Queue.Queue()

class Tabbed(QtGui.QTabWidget, tabbed_ui.Ui_TabWidget):
    def __init__(self):
        super(Tabbed, self).__init__()
        self.setupUi(self)
        self.reader = OpcThread(queue)
        self.randomdata = RandomDataThread(queue)
        self.reader.start()
        self.worker = Worker(queue)
        self.worker.start()
        # self.connect(self.reader, QtCore.SIGNAL("mysignal(QStringList)"), self.on_read, QtCore.Qt.QueuedConnection)
        self.randomdata.randomdataSignal.connect(self.on_random_read, QtCore.Qt.QueuedConnection)
        self.reader.teplocomSignal.connect(self.on_teplocom_read, QtCore.Qt.QueuedConnection)
        self.reader.matrikonSignal.connect(self.on_matrikon_read, QtCore.Qt.QueuedConnection)
        self.reader.teplocomprodSignal.connect(self.on_prod_read, QtCore.Qt.QueuedConnection)
        self.goButton_1.clicked.connect(self.go)
        self.goButton_2.clicked.connect(self.go)
        self.goButton_3.clicked.connect(self.go)
        self.stopButton_1.clicked.connect(self.stop)
        self.stopButton_2.clicked.connect(self.stop)
        self.stopButton_3.clicked.connect(self.stop)
        self.reportOldButton.clicked.connect(partial(self.show_selectdate_window, self.old_))
        self.reportNewButton.clicked.connect(partial(self.show_selectdate_window, self.new_))
        # можно так:
        self.reportSNButton.clicked.connect(lambda: self.show_selectdate_window(self.sn_))
        self.gorandomButton_1.clicked.connect(self.randomdata.start)
        self.stoprandomButton_1.clicked.connect(self.randomdata.stop)
        self.gorandomButton_2.clicked.connect(self.randomdata.start)
        self.stoprandomButton_2.clicked.connect(self.randomdata.stop)
        self.gorandomButton_3.clicked.connect(self.randomdata.start)
        self.stoprandomButton_3.clicked.connect(self.randomdata.stop)

        self.teplocomButton.clicked.connect(self.reader.get_teplocom)
        self.teplocom_2Button.clicked.connect(self.reader.get_prod_teplocom)
        self.matrikonButton.clicked.connect(self.reader.get_matrikon)
        self.activateButton.clicked.connect(self.activate_opc_buttons)
        
        self.teplocomButton.setDisabled(True)
        self.matrikonButton.setDisabled(True)
        self.teplocom_2Button.setDisabled(True)
        # self.pyshList.listSignal[list, int, str, str].connect(self.on_list_read, QtCore.Qt.QueuedConnection)
        self.setMinimumSize(1870, 900)

        self.lineEdits_toolTip_dic = dict(zip([key if "lineEdit_" in key else "" for key in self.__dict__.keys()],\
                                              [value.toolTip() if "lineEdit_" in key else "" for key, value in self.__dict__.items()]\
                                             )\
                                         )
        del self.lineEdits_toolTip_dic[""]


        """import schedule
        import time

        def job():
            print("I'm working...")

        schedule.every(10).minutes.do(job)
        schedule.every().hour.do(job)
        schedule.every().day.at("10:30").do(job)
        schedule.every().monday.do(job)
        schedule.every().wednesday.at("13:15").do(job)
        schedule.every().minute.at(":17").do(job)

        while True:
            schedule.run_pending()
            time.sleep(1)
        """
        # schedule.every(5).seconds.do(self.silent_report)
        schedule.every().day.at("07:00").do(self.silent_report)
        # Timer
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(schedule.run_pending)
        self.timer.start()
        
        self.verticalSlider_New.sliderMoved.connect(self.change_level_slider)
        self.verticalSlider_Old.sliderMoved.connect(self.change_level_slider)
        self.lineEdit_New_Level.setText("0.00")
        self.lineEdit_Old_Level.setText("0.00")
        # position of the left top point of full_bak_image from where to draw empty_bak_image:
        self.new_bak_left = self.label_BakFull_New.geometry().left()
        self.new_bak_top =  self.label_BakFull_New.geometry().top()
        self.old_bak_left = self.label_BakFull_Old.geometry().left()
        self.old_bak_top =  self.label_BakFull_Old.geometry().top()

        # self.lineEdit_Old_800PressureTPK2.setText("0000.22")
        # self.lineEdit_Old_800PressureTPK2.setStatusTip("0.22 statusTip")
        # self.lineEdit_Old_800PressureTPK2.setToolTip(self.lineEdit_Old_800PressureTPK2.toolTip() + " toolTip")

    def go(self):
        self.reader.start()

    def stop(self):
        self.reader.stop()

    def on_random_read(self, data_dic):
        for i in range(len(data_dic["values"])):
            self.__getattribute__(data_dic["lineEdit"][i]).setText(data_dic["values"][i])

    def activate_opc_buttons(self):
        if self.teplocomButton.isEnabled():
            self.teplocomButton.setDisabled(True)
            self.teplocom_2Button.setDisabled(True)
            self.matrikonButton.setDisabled(True)
            self.activateButton.setText("Enable buttons")
            self.lineEdit_New_TPK1TempBack.setStyleSheet("background-color: rgb(170, 255, 255);")
        else:
            self.teplocomButton.setDisabled(False)
            self.teplocom_2Button.setDisabled(False)
            self.matrikonButton.setDisabled(False)
            self.activateButton.setText("Disable buttons")
            self.lineEdit_New_TPK1TempBack.setStyleSheet("background-color: rgb(255, 170, 255);")

    def on_teplocom_read(self, teplocom_response):
        self.lineEdit_to_object = {}
        for name in self.reader.teplocom_tag_map.values():
            self.lineEdit_to_object[name] = self.__dict__[name]
        for tag in teplocom_response:
            tag_name, tag_value, tag_status, time = tag
            print tag_name, tag_value, tag_status, time
            # lineEdit_name = self.reader.teplocom_tag_map[tag_name]
            # self.lineEdit_to_object[lineEdit_name].setText(str(tag_value))
        print("-"*100)

    def on_matrikon_read(self, result):
        for tag in result:
            print tag

    def on_prod_read(self, prod_dic):
        for line_edit, tag_value in prod_dic.items():
            value = tag_value[0]
            status = tag_value[1]
            string_value = str(round(value, 2))
            self.__getattribute__(line_edit).setText(string_value)
            if status == "Good":
                self.__getattribute__(line_edit).setStyleSheet("background-color:powderblue;")
                self.__getattribute__(line_edit).setToolTip(self.lineEdits_toolTip_dic[line_edit])
            else:
                self.__getattribute__(line_edit).setStyleSheet("background-color: rgb(255, 170, 255);")
                self.__getattribute__(line_edit).setToolTip(u"Недостоверность:\n%s"%self.lineEdits_toolTip_dic[line_edit])
        self.change_level_prod(prod_dic["lineEdit_New_Level"][0])


    def change_level_prod(self, value):
        self.bak_image_height = BAK_IMAGE_HEIGHT
        self.bak_height = BAK_HEIGHT # real level in meters
        self.pixel_level = float(value)/self.bak_height*self.bak_image_height
        self.geometry_new_bak = QtCore.QRect(self.new_bak_left,\
                                                self.new_bak_top,\
                                                251,\
                                                self.bak_image_height - self.pixel_level)
        self.geometry_old_bak = QtCore.QRect(self.old_bak_left,\
                                                self.old_bak_top,\
                                                251,\
                                                self.bak_image_height - self.pixel_level)
        self.label_BakEmpty_New.setGeometry(self.geometry_new_bak)
        self.label_BakEmpty_Old.setGeometry(self.geometry_old_bak)
        if value > 5.82:
            self.lineEdit_New_Level.setStyleSheet("background-color: transparent; color: paleturquoise;") # lightgreen, skyblue
            self.lineEdit_Old_Level.setStyleSheet("background-color: transparent; color: paleturquoise;")
        else:
            self.lineEdit_New_Level.setStyleSheet("background-color: transparent;")
            self.lineEdit_Old_Level.setStyleSheet("background-color: transparent;")
            
    def change_level_slider(self, value):
        self.bak_image_height = BAK_IMAGE_HEIGHT
        self.bak_height = BAK_HEIGHT # real level in meters
        self.scale_value = 99 # slider max value
        # scaling slider value to image height in pixels:
        self.pixel_level =  float(value)/self.scale_value*self.bak_image_height
        self.geometry_new_bak = QtCore.QRect(self.new_bak_left,\
                                                self.new_bak_top,\
                                                251,\
                                                self.bak_image_height - self.pixel_level)
        self.geometry_old_bak = QtCore.QRect(self.old_bak_left,\
                                                self.old_bak_top,\
                                                251,\
                                                self.bak_image_height - self.pixel_level)
        self.label_BakEmpty_New.setGeometry(self.geometry_new_bak)
        self.label_BakEmpty_Old.setGeometry(self.geometry_old_bak)
        # scaling pixel level to real level in meters for indication:
        self.level_value_string = str(round((self.pixel_level/self.bak_image_height)*self.bak_height, 2))
        self.lineEdit_New_Level.setText(self.level_value_string)
        self.lineEdit_Old_Level.setText(self.level_value_string)
        if self.pixel_level/self.bak_image_height*self.bak_height > 5.82:
            self.lineEdit_New_Level.setStyleSheet("background-color: transparent; color: paleturquoise;")
            self.lineEdit_Old_Level.setStyleSheet("background-color: transparent; color: paleturquoise;")
        else:
            self.lineEdit_New_Level.setStyleSheet("background-color: transparent;")
            self.lineEdit_Old_Level.setStyleSheet("background-color: transparent;")

    def split_time(self, from_Qstring, to_Qstring):
        times = []
        from_time = datetime.strptime(str(from_Qstring), "%Y-%m-%d %H:%M:%S")
        to_time = datetime.strptime(str(to_Qstring), "%Y-%m-%d %H:%M:%S")
        difference = to_time - from_time
        # print "difference is:", difference
        minutes = timedelta(minutes=from_time.minute)
        seconds = timedelta(seconds=from_time.second)
        first_delta = timedelta(hours=1) if (seconds == 0 or minutes == 0) else timedelta(hours=1) - seconds - minutes
        hour = timedelta(hours=1)
        # print "to whole hour delta:", first_delta
        # print "minutes:",minutes
        # print "seconds:",seconds
        whole_from_time = from_time + first_delta
        # print "whole from time:", whole_from_time
        times.append(from_time)
        whole_time = whole_from_time
        # print 
        # print from_time
        delta = timedelta()
        while delta < difference - first_delta:
            # print whole_time
            times.append(whole_time)
            whole_time += hour
            delta += hour
        # print from_time + difference
        times.append(from_time + difference)
        return times

    def show_selectdate_window(self, tab):
        self.from_to_window = Report(tab)
        self.from_to_window.makePDFSignal.connect(self.put_pdf_task, QtCore.Qt.QueuedConnection)
        self.from_to_window.makeExcelSignal.connect(self.put_excel_task, QtCore.Qt.QueuedConnection)
        self.from_to_window.show()

    def prepare_querys(self, from_datetime, to_datetime, tab):
        self.from_time = from_datetime
        self.to_time = to_datetime
        self.tab = tab
        self.times = self.split_time(self.from_time, self.to_time)
        self.from_hour = datetime.strptime(str(self.from_time), "%Y-%m-%d %H:%M:%S").hour
        self.to_hour   = datetime.strptime(str(self.to_time), "%Y-%m-%d %H:%M:%S").hour
        self.querys = []

        for i in range(1, len(self.times)):
            # print "%s \t %s"%(self.times[i-1], self.times[i].strftime("%d %B %Y %H:%M"))

            self.querys.append({"time": self.times[i-1], "query": """\
            SELECT name, round(avg(value), 3) as avg_value,\
            datetime("%s") as hour, report_order FROM
            (SELECT * FROM vkt_data WHERE timestamp > datetime("%s")\
            AND timestamp < datetime("%s")\
            AND scheme = '%s' AND quality = "Good" AND report_order > 0 AND test = 0)
            GROUP by name ORDER by report_order;"""%(str(self.times[i-1]), str(self.times[i-1]), str(self.times[i]),\
            self.tab)})


            # self.querys.append({"time": self.times[i-1], "query": """\
            # SELECT report_names.name, vkt.avarage, report_names.report_order FROM report_names
            # LEFT JOIN
            #   (SELECT name, round(avg(value), 3) as avarage,\
            #   datetime("%s") as hour, report_order FROM
            #     (SELECT * FROM vkt_data WHERE timestamp > datetime("%s")\
            #       AND timestamp < datetime("%s")\
            #       AND quality = "Good" AND report_order > 0 AND test = 0)
            #   GROUP by name) vkt
            # on vkt.name = report_names.name
            # WHERE report_names.scheme = '%s'
            # ORDER by report_names.report_order"""%(str(self.times[i-1]), str(self.times[i-1]), str(self.times[i]),\
            # self.tab)})

        return self.querys

    def put_pdf_task(self, from_datetime, to_datetime, tab):
        self.querys = self.prepare_querys(from_datetime, to_datetime, tab)
        self.pdf_task = PDFTask(self.querys, str(self.tab))
        self.pdf_task.readtaskSignal.connect(self.read_task_done, QtCore.Qt.QueuedConnection)
        queue.put(self.pdf_task)

    def put_excel_task(self, from_datetime, to_datetime, tab):
        self.querys = self.prepare_querys(from_datetime, to_datetime, tab)
        self.excel_task = ExcelTask(self.querys, str(self.tab))
        self.excel_task.readtaskSignal.connect(self.read_task_done, QtCore.Qt.QueuedConnection)
        queue.put(self.excel_task)

    def put_test_task(self, from_datetime, to_datetime, tab):
        self.querys = self.prepare_querys(from_datetime, to_datetime, tab)
        self.test_task = PDFTask(self.querys, str(self.tab))
        self.test_task.readtaskSignal.connect(self.read_task_done, QtCore.Qt.QueuedConnection)
        queue.put(self.test_task)

    def read_task_done(self, silent, filename):
        print "silent: %s; filename: %s"%(silent, filename)
        if not silent:
            webbrowser.open(filename)

    def silent_report(self):
        for scheme in ["old_", "new_", "sn_"]:
            self.querys = self.prepare_querys(datetime.strftime(datetime.now() - timedelta(1), "%Y-%m-%d 00:00:00"),\
                                              datetime.strftime(datetime.now() - timedelta(1), "%Y-%m-%d 23:59:59"),\
                                              scheme)
            self.task = ExcelTask(self.querys, scheme, silent=True)
            self.task.readtaskSignal.connect(self.read_task_done, QtCore.Qt.QueuedConnection)
            queue.put(self.task)
        # print "real time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # print "from time:", datetime.now().strftime("%Y-%m-%d 00:00:00")
        # print "to time:", datetime.now().strftime("%Y-%m-%d %H:00:00")
        # print "-"*100


def main():
    app = QtGui.QApplication(sys.argv)
    icon = QtGui.QIcon()
    icon.addFile("invader.ico", QtCore.QSize(16,16))
    app.setWindowIcon(icon)
    window = Tabbed()
    window.showMaximized()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
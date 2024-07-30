# coding: utf-8
import os
import random
import sqlite3
import string
import sys
import webbrowser
import xlwt
from datetime import datetime
from PyQt4 import QtCore
import pdf

tab_map = {"old_": "OLD", "new_": "NEW", "sn_": "SN"}
# to choose sum or avarage value in footer (0 for avarage, 1 for sum):
old_footer_order = {0:0, 1:0, 2:0, 3:0, 4:1, 5:1, 6:1, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:1, 14:1, 15:1, 16:1,\
                    17:0, 18:0, 19:0, 20:0, 21:1, 22:1, 23:1, 24:1, 25:1}

new_footer_order = {0:0, 1:0, 2:0, 3:0, 4:1, 5:1, 6:1, 7:0, 8:0, 9:0, 10:0, 11:1, 12:1, 13:1, 14:0, 15:0, 16:0,\
                    17:0, 18:1, 19:1, 20:1, 21:0, 22:0, 23:0, 24:0, 25:1, 26:1, 27:1, 28:0, 29:0, 30:0, 31:0,\
                    32:1, 33:1, 34:1, 35:1, 36:1}

sn_footer_order = {0:1, 1:1, 2:1, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:1, 10:1, 11:0, 12:1, 13:0, 14:1, 15:1, 16:0,\
                   17:1, 18:0, 19:1}

footer_function_map = {"old_": old_footer_order, "new_": new_footer_order, "sn_": sn_footer_order}

sheetname_map = {"OLD" : u"Старый теплоучёт", "NEW" : u"Новый теплоучёт", "SN" : u"Собственные нужды"}


class ReadTask(QtCore.QObject):
    readtaskSignal = QtCore.pyqtSignal(bool, str)
    def __init__(self, sql, tab, silent=False):
        super(ReadTask, self).__init__()
        self.sql = sql
        self.tab = tab
        self.type = tab_map[self.tab]
        self.silent = silent

    def run(self):
        pass

    def generate_filename(self, extension, salt=""):
        basedir = os.path.dirname(sys.argv[0])
        reports_dir =  os.path.join(os.path.dirname(sys.argv[0]),"reports")
        if not os.path.exists(reports_dir):
            os.mkdir(reports_dir)
        s = string.ascii_letters # + string.digits
        salt = salt if salt else "".join(random.choice(s) for i in range(10))
        date_time = datetime.now().strftime("%Y%m%d_%H%M")
        type_extension = "%s.%s"%(self.type, extension)
        filename = os.path.join(reports_dir, "_".join([date_time, salt, type_extension]))
        return filename
    
    def translate_time_string(self, timestring):
        self.timestring = timestring
        self.months = [(u"January", u"января"), (u"February", u"февраля"), (u"March", u"марта"),\
                        (u"April", u"апреля"), (u"May", u"мая"), (u"June", u"июня"), \
                        (u"July", u"июля"), (u"August", u"августа"), (u"September", u"сентября"), \
                        (u"October", u"октября"), (u"November", u"ноября"), (u"December", u"декабря"), ]
        for en, ru in self.months:
            self.timestring = self.timestring.replace(en, ru)
        return self.timestring


class PDFTask(ReadTask):
    def __init__(self, sql, tab, silent=False):
        super(PDFTask, self).__init__(sql, tab, silent)

    def run(self):
        print "start report %s"%self.type
        if self.type == "NEW":
            self.pdf = pdf.NEW_SCHEME()
        elif self.type == "OLD":
            self.pdf = pdf.OLD_SCHEME()
        elif self.type == "SN":
            self.pdf = pdf.SN_SCHEME()
        else:
            self.pdf = None
        self.connection = sqlite3.connect("vkt.db")
        self.cursor = self.connection.cursor()

        if self.pdf is not None:
            self.pdf_name = self.generate_filename("pdf", salt="daily" if self.silent else "")
            print self.pdf_name
            self.all_values = []
            for query in self.sql:
                q = query["query"]
                # print q
                self.cursor.execute(q)
                result = None
                try:
                    result = self.cursor.fetchall()
                except:
                    print "чето не получилось..."
                finally:
                    # self.cursor.close()
                    pass
                if result:
                    self.line_values = []
                    self.timestring = self.translate_time_string(query["time"].strftime("%d %B %Y"))
                    self.timestring += u"г. "
                    self.timestring += query["time"].strftime("%H:%M")
                    print self.timestring
                    self.pdf.cell(pdf.TIME_WIDTH, pdf.HEIGHT, self.timestring, 1, pdf.right)
                    for line in result:
                        self.pdf.cell(pdf.DIRECTION_WIDTH, pdf.HEIGHT, str(line[1]), 1, pdf.right, align="R")
                        self.line_values.append(line[1])
                    self.pdf.ln()
                    self.all_values.append(self.line_values)
            self.z = zip(*self.all_values)
            self.sums = map(sum, self.z) # sums
            self.avarages = map(lambda x: round(float(sum(x))/len(x), 3), self.z) # avarages
            # choosing sum or avarage value:
            self.footer_function = footer_function_map[self.tab]
            self.avarages_and_sums = zip(self.avarages, self.sums)
            # print self.avarages_and_sums
            self.pdf.cell(pdf.TIME_WIDTH, pdf.HEIGHT, u"Итоги:", 1, pdf.right, align="R")
            for i in range(len(self.avarages_and_sums)):
                self.pdf.cell(pdf.DIRECTION_WIDTH,\
                                pdf.HEIGHT,\
                                str(self.avarages_and_sums[i][self.footer_function[i]]),\
                                1, pdf.right, align="R")
            self.pdf.ln()
            self.pdf.output(self.pdf_name)
            # webbrowser.open(self.pdf_name)
        else:
            print "no pdf"
        self.readtaskSignal.emit(self.silent, self.pdf_name)


class ExcelTask(ReadTask):
    def __init__(self, sql, tab, silent=False):
        super(ExcelTask, self).__init__(sql, tab, silent)

    def run(self):
        print "start excel report %s"%self.type
        self.wb = xlwt.Workbook()
        # self.sheet = self.wb.add_sheet(u"%s"%self.type)

        self.make_header(self.wb)

        self.connection = sqlite3.connect("vkt.db")
        self.cursor = self.connection.cursor()

        self.excel_name = self.generate_filename("xls", salt="daily" if self.silent else "")
        print self.excel_name

        self.all_values = []
        self.row_number = 3
        for query in self.sql:
            q = query["query"]
            # print q
            self.cursor.execute(q)
            result = None
            try:
                result = self.cursor.fetchall()
            except:
                print "чето не получилось..."
            finally:
                # self.cursor.close()
                pass

            if result:
                self.line_values = []
                self.timestring = self.translate_time_string(query["time"].strftime("%d %B %Y"))
                self.timestring += u"г. "
                self.timestring += query["time"].strftime("%H:%M")
                print self.timestring
                self.sheet.write(self.row_number, 0, self.timestring)
                self.col_number = len(result)
                for j in range(self.col_number):
                    self.sheet.write(self.row_number, j + 1, result[j][1])
                    self.line_values.append(result[j][1])
                self.all_values.append(self.line_values)
            else:
                continue
            self.row_number += 1

        self.z = zip(*self.all_values)
        self.sums = map(sum, self.z) # sums
        self.avarages = map(lambda x: round(float(sum(x))/len(x), 3), self.z) # avarages
        
        # choosing sum or avarage value:
        self.footer_function = footer_function_map[self.tab]
        self.avarages_and_sums = zip(self.avarages, self.sums)
        # print self.avarages_and_sums
        self.sheet.write(self.row_number, 0, u"Итоги:")
        for i in range(len(self.avarages_and_sums)):
            self.sheet.write(self.row_number, i + 1, self.avarages_and_sums[i][self.footer_function[i]])
        
        self.wb.save(self.excel_name)
        # webbrowser.open(self.excel_name)
        self.readtaskSignal.emit(self.silent, self.excel_name)

    def make_header(self, workbook):
        self.sheet = workbook.add_sheet(sheetname_map[self.type])
        style = xlwt.Style.easyxf("border: top thin, right thin, bottom thin, left thin;\
                                   align: vertical center, horizontal center, wrap 1")
        self.sheet.write_merge(0,2, 0,0, u"Время", style=style)

        if self.type == "NEW":
            # NEW:
            self.sheet.write_merge(0,0, 1,6, u"ДУ-1000", style=style)
            self.sheet.write_merge(1,1, 1,2, u"Температура", style=style)
            self.sheet.write_merge(1,1, 3,4, u"Давление", style=style)
            self.sheet.write_merge(1,1, 5,6, u"Расход", style=style)
            self.sheet.write(2,1, u"Прямая", style=style)
            self.sheet.write(2,2, u"Обратная", style=style)
            self.sheet.write(2,3, u"Прямая", style=style)
            self.sheet.write(2,4, u"Обратная", style=style)
            self.sheet.write(2,5, u"Прямая", style=style)
            self.sheet.write(2,6, u"Обратная", style=style)
            self.sheet.write_merge(0,2, 7,7, u"ДУ-1000 Гкал", style=style)

            self.sheet.write_merge(0,0, 8,13, u"ДУ-800", style=style)
            self.sheet.write_merge(1,1, 8,9, u"Температура", style=style)
            self.sheet.write_merge(1,1, 10,11, u"Давление", style=style)
            self.sheet.write_merge(1,1, 12,13, u"Расход", style=style)
            self.sheet.write(2,8, u"Прямая", style=style)
            self.sheet.write(2,9, u"Обратная", style=style)
            self.sheet.write(2,10, u"Прямая", style=style)
            self.sheet.write(2,11, u"Обратная", style=style)
            self.sheet.write(2,12, u"Прямая", style=style)
            self.sheet.write(2,13, u"Обратная", style=style)
            self.sheet.write_merge(0,2, 14,14, u"ДУ-800 Гкал", style=style)

            self.sheet.write_merge(0,0, 15,20, u"ДУ-400", style=style)
            self.sheet.write_merge(1,1, 15,16, u"Температура", style=style)
            self.sheet.write_merge(1,1, 17,18, u"Давление", style=style)
            self.sheet.write_merge(1,1, 19,20, u"Расход", style=style)
            self.sheet.write(2,15, u"Прямая", style=style)
            self.sheet.write(2,16, u"Обратная", style=style)
            self.sheet.write(2,17, u"Прямая", style=style)
            self.sheet.write(2,18, u"Обратная", style=style)
            self.sheet.write(2,19, u"Прямая", style=style)
            self.sheet.write(2,20, u"Обратная", style=style)
            self.sheet.write_merge(0,2, 21,21, u"ДУ-400 Гкал", style=style)

            self.sheet.write_merge(0,0, 22,27, u"ТПК-1", style=style)
            self.sheet.write_merge(1,1, 22,23, u"Температура", style=style)
            self.sheet.write_merge(1,1, 24,25, u"Давление", style=style)
            self.sheet.write_merge(1,1, 26,27, u"Расход", style=style)
            self.sheet.write(2,22, u"Прямая", style=style)
            self.sheet.write(2,23, u"Обратная", style=style)
            self.sheet.write(2,24, u"Прямая", style=style)
            self.sheet.write(2,25, u"Обратная", style=style)
            self.sheet.write(2,26, u"Прямая", style=style)
            self.sheet.write(2,27, u"Обратная", style=style)
            self.sheet.write_merge(0,2, 28,28, u"ТПК-1 Гкал", style=style)

            self.sheet.write_merge(0,0, 29,34, u"УЮН", style=style)
            self.sheet.write_merge(1,1, 29,30, u"Температура", style=style)
            self.sheet.write_merge(1,1, 31,32, u"Давление", style=style)
            self.sheet.write_merge(1,1, 33,34, u"Расход", style=style)
            self.sheet.write(2,29, u"Прямая", style=style)
            self.sheet.write(2,30, u"Обратная", style=style)
            self.sheet.write(2,31, u"Прямая", style=style)
            self.sheet.write(2,32, u"Обратная", style=style)
            self.sheet.write(2,33, u"Прямая", style=style)
            self.sheet.write(2,34, u"Обратная", style=style)
            self.sheet.write_merge(0,2, 35,35, u"УЮН Гкал", style=style)

            self.sheet.write_merge(0,2, 36,36, u"Подпитка", style=style)
            self.sheet.write_merge(0,2, 37,37, u"Гкал общ", style=style)

        elif self.type == "OLD":
            # OLD:
            self.sheet.write_merge(0,0, 1,6, u"ДУ-1000", style=style)
            self.sheet.write_merge(1,1, 1,2, u"Температура", style=style)
            self.sheet.write_merge(1,1, 3,4, u"Давление", style=style)
            self.sheet.write_merge(1,1, 5,6, u"Расход", style=style)
            self.sheet.write(2,1, u"Прямая", style=style)
            self.sheet.write(2,2, u"Обратная", style=style)
            self.sheet.write(2,3, u"Прямая", style=style)
            self.sheet.write(2,4, u"Обратная", style=style)
            self.sheet.write(2,5, u"Прямая", style=style)
            self.sheet.write(2,6, u"Обратная", style=style)
            self.sheet.write_merge(0,2, 7,7, u"ДУ-1000 Гкал", style=style)

            self.sheet.write_merge(0,0, 8,16, u"ДУ-800", style=style)
            self.sheet.write_merge(1,1, 8,10, u"Температура", style=style)
            self.sheet.write_merge(1,1, 11,13, u"Давление", style=style)
            self.sheet.write_merge(1,1, 14,16, u"Расход", style=style)
            self.sheet.write(2,8, u"Город", style=style)
            self.sheet.write(2,9, u"УЮН", style=style)
            self.sheet.write(2,10, u"Обратная", style=style)
            self.sheet.write(2,11, u"Город", style=style)
            self.sheet.write(2,12, u"УЮН", style=style)
            self.sheet.write(2,13, u"Обратная", style=style)
            self.sheet.write(2,14, u"Город", style=style)
            self.sheet.write(2,15, u"УЮН", style=style)
            self.sheet.write(2,16, u"Обратная", style=style)
            self.sheet.write_merge(0,2, 17,17, u"ДУ-800 Гкал", style=style)

            self.sheet.write_merge(0,0, 18,23, u"ТПК-1", style=style)
            self.sheet.write_merge(1,1, 18,19, u"Температура", style=style)
            self.sheet.write_merge(1,1, 20,21, u"Давление", style=style)
            self.sheet.write_merge(1,1, 22,23, u"Расход", style=style)
            self.sheet.write(2,18, u"Прямая", style=style)
            self.sheet.write(2,19, u"Обратная", style=style)
            self.sheet.write(2,20, u"Прямая", style=style)
            self.sheet.write(2,21, u"Обратная", style=style)
            self.sheet.write(2,22, u"Прямая", style=style)
            self.sheet.write(2,23, u"Обратная", style=style)
            self.sheet.write_merge(0,2, 24,24, u"ТПК-1 Гкал", style=style)

            self.sheet.write_merge(0,2, 25,25, u"Подпитка", style=style)
            self.sheet.write_merge(0,2, 26,26, u"Гкал общ", style=style)

        elif self.type == "SN":
            # SN:
            self.sheet.write_merge(0,0, 1,10, u"Собственные нужды", style=style)
            self.sheet.write_merge(1,2, 1,1, u"М под., т\\ч", style=style)
            self.sheet.write_merge(1,2, 2,2, u"М обр., т\\ч", style=style)
            self.sheet.write_merge(1,2, 3,3, u"dМ, т\\ч", style=style)
            self.sheet.write_merge(1,2, 4,4, u"T под., °C", style=style)
            self.sheet.write_merge(1,2, 5,5, u"T обр., °C", style=style)
            self.sheet.write_merge(1,2, 6,6, u"dT, °C", style=style)
            self.sheet.write_merge(1,2, 7,7, u"P под., МПа", style=style)
            self.sheet.write_merge(1,2, 8,8, u"P обр., МПа", style=style)
            self.sheet.write_merge(1,2, 9,9, u"dP, МПа", style=style)
            self.sheet.write_merge(1,2, 10,10, u"Q, Гкал", style=style)

            self.sheet.write_merge(0,0, 11,12, u"Подпитка ТС", style=style)
            self.sheet.write_merge(0,0, 13,14, u"ДСВ400", style=style)
            self.sheet.write(0,15, u"ТС - ДСВ400", style=style)
            self.sheet.write_merge(0,0, 16,17, u"ХОВ1", style=style)
            self.sheet.write_merge(0,0, 18,19, u"ХОВ2", style=style)
            self.sheet.write(0,20, u"ХОВ1 + ХОВ2", style=style)

            self.sheet.write_merge(1,2, 11,11, u"M, т\\ч", style=style)
            self.sheet.write_merge(1,2, 12,12, u"T, °C", style=style)
            self.sheet.write_merge(1,2, 13,13, u"M, т\\ч", style=style)
            self.sheet.write_merge(1,2, 14,14, u"T, °C", style=style)
            self.sheet.write_merge(1,2, 15,15, u"dМ, т\\ч", style=style)
            self.sheet.write_merge(1,2, 16,16, u"M, т\\ч", style=style)
            self.sheet.write_merge(1,2, 17,17, u"T, °C", style=style)
            self.sheet.write_merge(1,2, 18,18, u"M, т\\ч", style=style)
            self.sheet.write_merge(1,2, 19,19, u"T, °C", style=style)
            self.sheet.write_merge(1,2, 20,20, u"M, т\\ч", style=style)
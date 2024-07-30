# coding: utf-8
import random
import webbrowser
from fpdf import FPDF

OLD_DOCUMENT_WIDTH = 580
OLD_DOCUMENT_HEIGHT = 210

NEW_DOCUMENT_WIDTH = 800
NEW_DOCUMENT_HEIGHT = 210

SN_DOCUMENT_WIDTH = 460
SN_DOCUMENT_HEIGHT = 210

HEIGHT = 5
TALL = HEIGHT*3
TIME_WIDTH = 32
GKAL_WIDTH = 20
DIRECTION_WIDTH = 20 # 17
TWO_PARAMETER_WIDTH = DIRECTION_WIDTH*2
THREE_PARAMETER_WIDTH = DIRECTION_WIDTH*3
TWO_PIPE_WIDTH = TWO_PARAMETER_WIDTH*3
THREE_PIPE_WIDTH = THREE_PARAMETER_WIDTH*3

right = 0
newline = 1
under = 2


class  PDF(FPDF):
    def __init__(self, *args, **kwargs):
        super(PDF, self).__init__(*args, **kwargs)
        self.add_font("FreeSerifBold", "", "C:\\Python27\\Lib\\site-packages\\fpdf\\font\\FreeSerifBold.ttf", uni=True)
        self.add_font("FreeSerif", "", "C:\\Python27\\Lib\\site-packages\\fpdf\\font\\FreeSerif.ttf" , uni=True)
        self.set_font("FreeSerif", "", 8)
        self.add_page()

    def footer(self):
        self.set_y(-15)
        self.set_text_color(128) # Text color in gray
        self.cell(0, 10, 'Страница ' + str(self.page_no()), 0, 0, 'C')        


class OLD_SCHEME(PDF):
    def __init__(self, *args, **kwargs):
        super(OLD_SCHEME, self).__init__("L", unit="mm", format=(OLD_DOCUMENT_HEIGHT, OLD_DOCUMENT_WIDTH),*args, **kwargs)
        self.type = "OLD_"

    def header(self):
        self.set_font("FreeSerifBold", "", 8)

        self.cell(TIME_WIDTH, TALL, "Время", 1, right, "C")
        self.cell(TWO_PIPE_WIDTH, HEIGHT, "ДУ-1000", 1, newline, "C")
        self.set_xy(self.get_x() + TIME_WIDTH, self.get_y())
        self.cell(TWO_PARAMETER_WIDTH, HEIGHT, "Температура", 1, right, "C")
        self.cell(TWO_PARAMETER_WIDTH, HEIGHT, "Давление", 1, right, "C")
        self.cell(TWO_PARAMETER_WIDTH, HEIGHT, "Расход", 1, newline, "C")
        self.set_xy(self.get_x() + TIME_WIDTH, self.get_y())
        for i in range(3):
            self.cell(DIRECTION_WIDTH, HEIGHT, "Прямая", 1, right, "C")
            self.cell(DIRECTION_WIDTH, HEIGHT, "Обратная", 1, right, "C")
        self.set_xy(self.get_x(), self.get_y() - HEIGHT*2)
        self.cell(GKAL_WIDTH, TALL, u"ДУ-1000 Гкал", 1, right, "C")

        self.cell(THREE_PIPE_WIDTH, HEIGHT, "ДУ-800", 1, newline, "C")
        self.set_xy(self.get_x() + TIME_WIDTH + TWO_PIPE_WIDTH + GKAL_WIDTH, self.get_y())
        self.cell(THREE_PARAMETER_WIDTH, HEIGHT, "Температура", 1, right, "C")
        self.cell(THREE_PARAMETER_WIDTH, HEIGHT, "Давление", 1, right, "C")
        self.cell(THREE_PARAMETER_WIDTH, HEIGHT, "Расход", 1, newline, "C")
        self.set_xy(self.get_x() + TIME_WIDTH + TWO_PIPE_WIDTH + GKAL_WIDTH, self.get_y())
        for i in range(3):
            self.cell(DIRECTION_WIDTH, HEIGHT, "Город", 1, right, "C")
            self.cell(DIRECTION_WIDTH, HEIGHT, "УЮН", 1, right, "C")
            self.cell(DIRECTION_WIDTH, HEIGHT, "Обратная", 1, right, "C")
        self.set_xy(self.get_x(), self.get_y() - HEIGHT*2)
        self.cell(GKAL_WIDTH, TALL, u"ДУ-800 Гкал", 1, right, "C")

        self.cell(TWO_PIPE_WIDTH, HEIGHT, "ТПК-1", 1, newline, "C")
        self.set_xy(self.get_x() + TIME_WIDTH + TWO_PIPE_WIDTH + THREE_PIPE_WIDTH + GKAL_WIDTH*2, self.get_y())
        self.cell(TWO_PARAMETER_WIDTH, HEIGHT, "Температура", 1, right, "C")
        self.cell(TWO_PARAMETER_WIDTH, HEIGHT, "Давление", 1, right, "C")
        self.cell(TWO_PARAMETER_WIDTH, HEIGHT, "Расход", 1, newline, "C")
        self.set_xy(self.get_x() + TIME_WIDTH + TWO_PIPE_WIDTH + THREE_PIPE_WIDTH + GKAL_WIDTH*2, self.get_y())
        for i in range(3):
            self.cell(DIRECTION_WIDTH, HEIGHT, "Прямая", 1, right, "C")
            self.cell(DIRECTION_WIDTH, HEIGHT, "Обратная", 1, right, "C")
        self.set_xy(self.get_x(), self.get_y() - HEIGHT*2)
        self.cell(GKAL_WIDTH, TALL, "ТПК-1 Гкал", 1, right, "C")

        self.cell(GKAL_WIDTH, TALL, "Подпитка", 1, right, "C")
        self.cell(GKAL_WIDTH, TALL, "Гкал общ", 1, right, "C")

        self.ln()


class NEW_SCHEME(PDF):
    def __init__(self, *args, **kwargs):
        super(NEW_SCHEME, self).__init__("L", unit="mm", format=(NEW_DOCUMENT_HEIGHT, NEW_DOCUMENT_WIDTH),*args, **kwargs)
        self.type = "NEW_"

    def header(self):
        self.set_font("FreeSerifBold", "", 8)

        self.cell(TIME_WIDTH, TALL, "Время", 1, right, "C")
        self.cell(TWO_PIPE_WIDTH, HEIGHT, "ДУ-1000", 1, newline, "C")
        self.set_xy(self.get_x() + TIME_WIDTH, self.get_y())
        self.cell(TWO_PARAMETER_WIDTH, HEIGHT, "Температура", 1, right, "C")
        self.cell(TWO_PARAMETER_WIDTH, HEIGHT, "Давление", 1, right, "C")
        self.cell(TWO_PARAMETER_WIDTH, HEIGHT, "Расход", 1, newline, "C")
        self.set_xy(self.get_x() + TIME_WIDTH, self.get_y())
        for i in range(3):
            self.cell(DIRECTION_WIDTH, HEIGHT, "Прямая", 1, right, "C")
            self.cell(DIRECTION_WIDTH, HEIGHT, "Обратная", 1, right, "C")
        self.set_xy(self.get_x(), self.get_y() - HEIGHT*2)
        self.cell(GKAL_WIDTH, TALL, u"ДУ-1000 Гкал", 1, right, "C")

        self.cell(TWO_PIPE_WIDTH, HEIGHT, "ДУ-800", 1, newline, "C")
        self.set_xy(self.get_x() + TIME_WIDTH + TWO_PIPE_WIDTH + GKAL_WIDTH, self.get_y())
        self.cell(TWO_PARAMETER_WIDTH, HEIGHT, "Температура", 1, right, "C")
        self.cell(TWO_PARAMETER_WIDTH, HEIGHT, "Давление", 1, right, "C")
        self.cell(TWO_PARAMETER_WIDTH, HEIGHT, "Расход", 1, newline, "C")
        self.set_xy(self.get_x() + TIME_WIDTH + TWO_PIPE_WIDTH + GKAL_WIDTH, self.get_y())
        for i in range(3):
            self.cell(DIRECTION_WIDTH, HEIGHT, "Прямая", 1, right, "C")
            self.cell(DIRECTION_WIDTH, HEIGHT, "Обратная", 1, right, "C")
        self.set_xy(self.get_x(), self.get_y() - HEIGHT*2)
        self.cell(GKAL_WIDTH, TALL, u"ДУ-800 Гкал", 1, right, "C")

        self.cell(TWO_PIPE_WIDTH, HEIGHT, "ДУ-400", 1, newline, "C")
        self.set_xy(self.get_x() + TIME_WIDTH + TWO_PIPE_WIDTH*2 + GKAL_WIDTH*2, self.get_y())
        self.cell(TWO_PARAMETER_WIDTH, HEIGHT, "Температура", 1, right, "C")
        self.cell(TWO_PARAMETER_WIDTH, HEIGHT, "Давление", 1, right, "C")
        self.cell(TWO_PARAMETER_WIDTH, HEIGHT, "Расход", 1, newline, "C")
        self.set_xy(self.get_x() + TIME_WIDTH + TWO_PIPE_WIDTH*2 + GKAL_WIDTH*2, self.get_y())
        for i in range(3):
            self.cell(DIRECTION_WIDTH, HEIGHT, "Прямая", 1, right, "C")
            self.cell(DIRECTION_WIDTH, HEIGHT, "Обратная", 1, right, "C")
        self.set_xy(self.get_x(), self.get_y() - HEIGHT*2)
        self.cell(GKAL_WIDTH, TALL, "ДУ-400 Гкал", 1, right, "C")

        self.cell(TWO_PIPE_WIDTH, HEIGHT, "ТПК-1", 1, newline, "C")
        self.set_xy(self.get_x() + TIME_WIDTH + TWO_PIPE_WIDTH*3 + GKAL_WIDTH*3, self.get_y())
        self.cell(TWO_PARAMETER_WIDTH, HEIGHT, "Температура", 1, right, "C")
        self.cell(TWO_PARAMETER_WIDTH, HEIGHT, "Давление", 1, right, "C")
        self.cell(TWO_PARAMETER_WIDTH, HEIGHT, "Расход", 1, newline, "C")
        self.set_xy(self.get_x() + TIME_WIDTH + TWO_PIPE_WIDTH*3 + GKAL_WIDTH*3, self.get_y())
        for i in range(3):
            self.cell(DIRECTION_WIDTH, HEIGHT, "Прямая", 1, right, "C")
            self.cell(DIRECTION_WIDTH, HEIGHT, "Обратная", 1, right, "C")
        self.set_xy(self.get_x(), self.get_y() - HEIGHT*2)
        self.cell(GKAL_WIDTH, TALL, "ТПК-1 Гкал", 1, right, "C")

        self.cell(TWO_PIPE_WIDTH, HEIGHT, "УЮН", 1, newline, "C")
        self.set_xy(self.get_x() + TIME_WIDTH + TWO_PIPE_WIDTH*4 + GKAL_WIDTH*4, self.get_y())
        self.cell(TWO_PARAMETER_WIDTH, HEIGHT, "Температура", 1, right, "C")
        self.cell(TWO_PARAMETER_WIDTH, HEIGHT, "Давление", 1, right, "C")
        self.cell(TWO_PARAMETER_WIDTH, HEIGHT, "Расход", 1, newline, "C")
        self.set_xy(self.get_x() + TIME_WIDTH + TWO_PIPE_WIDTH*4 + GKAL_WIDTH*4, self.get_y())
        for i in range(3):
            self.cell(DIRECTION_WIDTH, HEIGHT, "Прямая", 1, right, "C")
            self.cell(DIRECTION_WIDTH, HEIGHT, "Обратная", 1, right, "C")
        self.set_xy(self.get_x(), self.get_y() - HEIGHT*2)

        self.cell(GKAL_WIDTH, TALL, "УЮН Гкал", 1, right, "C")
        self.cell(GKAL_WIDTH, TALL, "Подпитка", 1, right, "C")
        self.cell(GKAL_WIDTH, TALL, "Гкал общ", 1, right, "C")

        self.ln()


class SN_SCHEME(PDF):
    def __init__(self, *args, **kwargs):
        super(SN_SCHEME, self).__init__("L", unit="mm", format=(SN_DOCUMENT_HEIGHT, SN_DOCUMENT_WIDTH), *args, **kwargs)
        self.type = "SN_"

    def header(self):
        # self.add_font("FreeSerifBold", "", "FreeSerifBold.ttf", uni=True)
        self.set_font("FreeSerifBold", "", 8)

        self.cell(TIME_WIDTH, TALL - HEIGHT, "Время", 1, right, "C")
        self.cell(DIRECTION_WIDTH*10, HEIGHT, "Собственные нужды", 1, newline, "C")
        self.set_xy(self.get_x() + TIME_WIDTH, self.get_y())
        self.cell(DIRECTION_WIDTH, HEIGHT, "М под., т/ч", 1, right, "C")
        self.cell(DIRECTION_WIDTH, HEIGHT, "М обр., т/ч", 1, right, "C")
        self.cell(DIRECTION_WIDTH, HEIGHT, "dМ, т/ч", 1, right, "C")
        self.cell(DIRECTION_WIDTH, HEIGHT, "T под., °C", 1, right, "C")
        self.cell(DIRECTION_WIDTH, HEIGHT, "T обр., °C", 1, right, "C")
        self.cell(DIRECTION_WIDTH, HEIGHT, "dT, °C", 1, right, "C")
        self.cell(DIRECTION_WIDTH, HEIGHT, "P под., МПа", 1, right, "C")
        self.cell(DIRECTION_WIDTH, HEIGHT, "P обр., МПа", 1, right, "C")
        self.cell(DIRECTION_WIDTH, HEIGHT, "dP, МПа", 1, right, "C")
        self.cell(DIRECTION_WIDTH, HEIGHT, "Q, Гкал", 1, right, "C")

        self.set_xy(self.get_x(), self.get_y() - HEIGHT)
        self.cell(DIRECTION_WIDTH*2, HEIGHT, u"Подпитка ТС", 1, newline, "C")
        self.set_xy(self.get_x() + TIME_WIDTH + DIRECTION_WIDTH*10, self.get_y())
        self.cell(DIRECTION_WIDTH, HEIGHT, "M, т/ч", 1, right, "C")
        self.cell(DIRECTION_WIDTH, HEIGHT, "Т, °C", 1, right, "C")

        self.set_xy(self.get_x(), self.get_y() - HEIGHT)
        self.cell(DIRECTION_WIDTH*2, HEIGHT, u"ДСВ400", 1, newline, "C")
        self.set_xy(self.get_x() + TIME_WIDTH + DIRECTION_WIDTH*12, self.get_y())
        self.cell(DIRECTION_WIDTH, HEIGHT, "M, т/ч", 1, right, "C")
        self.cell(DIRECTION_WIDTH, HEIGHT, "Т, °C", 1, right, "C")

        self.set_xy(self.get_x(), self.get_y() - HEIGHT)
        self.cell(DIRECTION_WIDTH, HEIGHT, u"ТС - ДСВ400", 1, newline, "C")
        self.set_xy(self.get_x() + TIME_WIDTH + DIRECTION_WIDTH*14, self.get_y())
        self.cell(DIRECTION_WIDTH, HEIGHT, "dM, т/ч", 1, right, "C")
        
        self.set_xy(self.get_x(), self.get_y() - HEIGHT)
        self.cell(DIRECTION_WIDTH*2, HEIGHT, u"ХОВ1", 1, newline, "C")
        self.set_xy(self.get_x() + TIME_WIDTH + DIRECTION_WIDTH*15, self.get_y())
        self.cell(DIRECTION_WIDTH, HEIGHT, "M, т/ч", 1, right, "C")
        self.cell(DIRECTION_WIDTH, HEIGHT, "Т, °C", 1, right, "C")

        self.set_xy(self.get_x(), self.get_y() - HEIGHT)
        self.cell(DIRECTION_WIDTH*2, HEIGHT, u"ХОВ2", 1, newline, "C")
        self.set_xy(self.get_x() + TIME_WIDTH + DIRECTION_WIDTH*17, self.get_y())
        self.cell(DIRECTION_WIDTH, HEIGHT, "M, т/ч", 1, right, "C")
        self.cell(DIRECTION_WIDTH, HEIGHT, "Т, °C", 1, right, "C")

        self.set_xy(self.get_x(), self.get_y() - HEIGHT)
        self.cell(DIRECTION_WIDTH, HEIGHT, u"ХОВ1 + ХОВ2", 1, under, "C")
        self.cell(DIRECTION_WIDTH, HEIGHT, u"M, т/ч", 1, right, "C")

        self.ln()


if __name__ == "__main__":

    old_pdf = OLD_SCHEME()
    new_pdf = NEW_SCHEME()
    sn_pdf  = SN_SCHEME()     #"L", unit="mm", format=(SN_DOCUMENT_HEIGHT, SN_DOCUMENT_WIDTH))
    for i in range(1, 81):
        old_pdf.cell(TIME_WIDTH, HEIGHT, '30 сентября 2019г. %d:00'%i, 1, right)
        new_pdf.cell(TIME_WIDTH, HEIGHT, '30 сентября 2019г. %d:00'%i, 1, right)
        sn_pdf.cell(TIME_WIDTH, HEIGHT, '30 сентября 2019г. %d:00'%i, 1, right)

        for j in range(36):
            new_pdf.cell(DIRECTION_WIDTH, HEIGHT, str(round(random.random()*100,2)), 0, right, align="R")

        for j in range(25):
            old_pdf.cell(DIRECTION_WIDTH, HEIGHT, str(round(random.random()*100,2)), 0, right, align="R")

        for j in range(19):
            sn_pdf.cell(DIRECTION_WIDTH, HEIGHT, str(round(random.random()*100,2)), 0, right, align="R")

        sn_pdf.cell(DIRECTION_WIDTH, HEIGHT, "23SNNN", 0, newline, align="R")
        new_pdf.cell(DIRECTION_WIDTH, HEIGHT, "234NEW", 0, newline, align="R")
        old_pdf.cell(DIRECTION_WIDTH, HEIGHT, "234OLD", 0, newline, align="R")

    old_pdf.output("random_old.pdf")
    new_pdf.output("random_new.pdf")
    sn_pdf.output("random_sn.pdf")
    webbrowser.open("random_old.pdf")
    webbrowser.open("random_new.pdf")
    webbrowser.open("random_sn.pdf")


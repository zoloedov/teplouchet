# coding: utf-8
import random
import datetime
import random
import sqlite3
import Queue
from PyQt4 import QtCore
import OpenOPC
from parse_mopc import OpcTree
from tag_map_dic import new_lineEdits, old_lineEdits, new_TotallineEdits, old_TotallineEdits, sn_lineEdits

lineEdits = {"new_": new_lineEdits, "sn_": sn_lineEdits, "old_": old_lineEdits}

class OpcThread(QtCore.QThread):
    
    matrikonSignal = QtCore.pyqtSignal(list)
    teplocomSignal = QtCore.pyqtSignal(list)
    teplocomprodSignal = QtCore.pyqtSignal(dict)
    def __init__(self, queue):#, Tabbed):
        super(OpcThread, self).__init__()
        self.OPC_MATRIKON = "Matrikon.OPC.Simulation.1"
        self.OPC_TEPLOCOM = "InSAT.OPC.Teplocom.Da"
        self.queue = queue
        

        self.matrikon_tags = ["Random.Money", "Random.Int1",
                                "Random.Real8", "Saw-toothed Waves.Int4",
                                "Saw-toothed Waves.Real8", "Random.String",
                                "Random.Time", "Random.Qualities",
                                "Triangle Waves.Real4", "Triangle Waves.UInt4"
                                ]

        self.teplocom_tags =  [u"ВКТ-5:Все переменные:Текущие значения:Трубы:Труба 1:Температура:Значение",
                                u"ВКТ-5:Все переменные:Текущие значения:Трубы:Труба 1:Давление:Значение",
                                u"ВКТ-5:Все переменные:Текущие значения:Трубы:Труба 1:Расход:Значение",
                                u"ВКТ-5:Все переменные:Текущие значения:Тепловые вводы:Тв1:M:Значение",
                                u"ВКТ-5:Все переменные:Текущие значения:Тепловые вводы:Тв1:Q:Значение",
                                u"fasdfasdf"
                                ]

        self.teplocom_tag_map =\
                                {u"ВКТ-5:Все переменные:Текущие значения:Трубы:Труба 1:Температура:Значение":\
                                "lineEdit_SN_SNPressureBack",\
                                u"ВКТ-5:Все переменные:Текущие значения:Трубы:Труба 1:Давление:Значение":\
                                "lineEdit_SN_SNTempBack",\
                                u"ВКТ-5:Все переменные:Текущие значения:Трубы:Труба 1:Расход:Значение":\
                                "lineEdit_SN_HOV2FlowDM",\
                                u"ВКТ-5:Все переменные:Текущие значения:Тепловые вводы:Тв1:M:Значение":\
                                "lineEdit_SN_SNQ",\
                                u"ВКТ-5:Все переменные:Текущие значения:Тепловые вводы:Тв1:Q:Значение":\
                                "lineEdit_SN_HOV2TempDirect"}

        # self.teplocom_tags_2 = OpcTree("C:\\Users\\Zoloedov_is\\Desktop\\PyVKT\\test.m_opc").tags()

        self.report_order = {   #NEW: 37 in report
                                "lineEdit_New_1000Feed": -1,\
                                "lineEdit_New_1000FlowBack": 6,\
                                "lineEdit_New_1000FlowDirect": 5,\
                                "lineEdit_New_1000PressureBack": 4,\
                                "lineEdit_New_1000PressureDirect": 3,\
                                "lineEdit_New_1000TempBack": 2,\
                                "lineEdit_New_1000TempDirect": 1,\
                                "lineEdit_New_1000TvM": -1,\
                                "lineEdit_New_1000TvQ": 7,\
                                "lineEdit_New_400Feed": -1,\
                                "lineEdit_New_400FlowBack": 20,\
                                "lineEdit_New_400FlowDirect": 19,\
                                "lineEdit_New_400PressureBack": 18,\
                                "lineEdit_New_400PressureDirect": 17,\
                                "lineEdit_New_400TempBack": 16,\
                                "lineEdit_New_400TempDirect": 15,\
                                "lineEdit_New_400TvM": -1,\
                                "lineEdit_New_400TvQ": 21,\
                                "lineEdit_New_800Feed": -1,\
                                "lineEdit_New_800FlowDirect": 12,\
                                "lineEdit_New_800FlowBack": 13,\
                                "lineEdit_New_800PressureDirect": 10,\
                                "lineEdit_New_800PressureBack": 11,\
                                "lineEdit_New_800TempBack": 9,\
                                "lineEdit_New_800TempDirect": 8,\
                                "lineEdit_New_800TvM": -1,\
                                "lineEdit_New_800TvQ": 14,\
                                "lineEdit_New_Level": -1,\
                                "lineEdit_New_TPK1Feed": -1,\
                                "lineEdit_New_TPK1FlowBack": 27,\
                                "lineEdit_New_TPK1FlowDirect": 26,\
                                "lineEdit_New_TPK1PressureBack": 25,\
                                "lineEdit_New_TPK1PressureDirect": 24,\
                                "lineEdit_New_TPK1TempBack": 23,\
                                "lineEdit_New_TPK1TempDirect": 22,\
                                "lineEdit_New_TPK1TvM": -1,\
                                "lineEdit_New_TPK1TvQ": 28,\
                                "lineEdit_New_TPK2Feed": -1,\
                                "lineEdit_New_TPK2FlowBack": 34,\
                                "lineEdit_New_TPK2FlowDirect": 33,\
                                "lineEdit_New_TPK2PressureBack": 32,\
                                "lineEdit_New_TPK2PressureDirect": 31,\
                                "lineEdit_New_TPK2TempBack": 30,\
                                "lineEdit_New_TPK2TempDirect": 29,\
                                "lineEdit_New_TPK2TvM": -1,\
                                "lineEdit_New_TPK2TvQ": 35,\
                                "lineEdit_New_TotalFeed": -1,\
                                "lineEdit_New_TotalFlowBack": -1,\
                                "lineEdit_New_TotalFlowDirect": -1,\
                                "lineEdit_New_TotalTvM": 36,\
                                "lineEdit_New_TotalTvQ": 37,\
                                #OLD: 26 in report
                                "lineEdit_Old_1000Feed": -1,\
                                "lineEdit_Old_1000FlowBack": 6,\
                                "lineEdit_Old_1000FlowDirect": 5,\
                                "lineEdit_Old_1000PressureBack": 4,\
                                "lineEdit_Old_1000PressureDirect": 3,\
                                "lineEdit_Old_1000TempBack": 2,\
                                "lineEdit_Old_1000TempDirect": 1,\
                                "lineEdit_Old_1000TvHV": -1,\
                                "lineEdit_Old_1000TvM": -1,\
                                "lineEdit_Old_1000TvQ": 7,\
                                "lineEdit_Old_400Feed": -1,\
                                "lineEdit_Old_400FlowBack": 23,\
                                "lineEdit_Old_400FlowDirect": 22,\
                                "lineEdit_Old_400PressureBack": 21,\
                                "lineEdit_Old_400PressureDirect": 20,\
                                "lineEdit_Old_400TempBack": 19,\
                                "lineEdit_Old_400TempDirect": 18,\
                                "lineEdit_Old_400TvHV": -1,\
                                "lineEdit_Old_400TvM": -1,\
                                "lineEdit_Old_400TvQ": 24,\
                                "lineEdit_Old_800Feed": -1,\
                                "lineEdit_Old_800FlowBack": 16,\
                                "lineEdit_Old_800FlowDirect": 14,\
                                "lineEdit_Old_800FlowTPK2": 15,\
                                "lineEdit_Old_800PressureBack": 13,\
                                "lineEdit_Old_800PressureDirect": 11,\
                                "lineEdit_Old_800PressureTPK2": 12,\
                                "lineEdit_Old_800TempBack": 10,\
                                "lineEdit_Old_800TempDirect": 8,\
                                "lineEdit_Old_800TempTPK2": 9,\
                                "lineEdit_Old_800TvHV": -1,\
                                "lineEdit_Old_800TvM": -1,\
                                "lineEdit_Old_800TvQ": 17,\
                                "lineEdit_Old_Level": -1,\
                                "lineEdit_Old_TotalFeed": 25,\
                                "lineEdit_Old_TotalMBack": -1,\
                                "lineEdit_Old_TotalMDirect": -1,\
                                "lineEdit_Old_TotalQ": 26,\
                                #OLD: 20 in report
                                "lineEdit_SN_DSV400FlowDirect": 13,\
                                "lineEdit_SN_DSV400TempDirect": 14,\
                                "lineEdit_SN_FeedTSFlowDM": 15,\
                                "lineEdit_SN_FeedTSFlowDirect": 11,\
                                "lineEdit_SN_FeedTSTempDirect": 12,\
                                "lineEdit_SN_HOV1FlowDirect": 16,\
                                "lineEdit_SN_HOV1TempDirect": 17,\
                                "lineEdit_SN_HOV2FlowDM": 20,\
                                "lineEdit_SN_HOV2FlowDirect": 18,\
                                "lineEdit_SN_HOV2TempDirect": 19,\
                                "lineEdit_SN_Q1": -1,\
                                "lineEdit_SN_Q2": -1,\
                                "lineEdit_SN_SNFlowBack": 2,\
                                "lineEdit_SN_SNFlowDM": 3,\
                                "lineEdit_SN_SNFlowDirect": 1,\
                                "lineEdit_SN_SNPressureBack": 8,\
                                "lineEdit_SN_SNPressureDP": 9,\
                                "lineEdit_SN_SNPressureDirect": 7,\
                                "lineEdit_SN_SNQ": 10,\
                                "lineEdit_SN_SNTempBack": 5,\
                                "lineEdit_SN_SNTempDT": 6,\
                                "lineEdit_SN_SNTempDirect": 4\
                            }

        self.prod_dic = {  # NEW 40:
                            u"НовыйДУ1000:ALL:ТЗ:Тр:Тр1:t:Значение": "lineEdit_New_1000TempDirect",\
                            u"НовыйДУ1000:ALL:ТЗ:Тр:Тр1:P:Значение": "lineEdit_New_1000PressureDirect",\
                            u"НовыйДУ1000:ALL:ТЗ:Тр:Тр1:Расход:Значение": "lineEdit_New_1000FlowDirect",\
                            u"НовыйДУ1000:ALL:ТЗ:Тв:Тв1:Q:Значение": "lineEdit_New_1000TvQ",\
                            u"НовыйДУ1000:ALL:ТЗ:Тр:Тр2:t:Значение": "lineEdit_New_1000TempBack",\
                            u"НовыйДУ1000:ALL:ТЗ:Тр:Тр2:P:Значение": "lineEdit_New_1000PressureBack",\
                            u"НовыйДУ1000:ALL:ТЗ:Тр:Тр2:Расход:Значение": "lineEdit_New_1000FlowBack",\
                            u"НовыйДУ1000:ALL:ТЗ:Тв:Тв1:M:Значение": "lineEdit_New_1000TvM",\

                            u"НовыйДУ800:ALL:ТЗ:Тр:Тр1:t:Значение": "lineEdit_New_800TempDirect",\
                            u"НовыйДУ800:ALL:ТЗ:Тр:Тр1:P:Значение": "lineEdit_New_800PressureDirect",\
                            u"НовыйДУ800:ALL:ТЗ:Тр:Тр1:Расход:Значение": "lineEdit_New_1000FlowDirect",\
                            u"НовыйДУ800:ALL:ТЗ:Тв:Тв1:Q:Значение": "lineEdit_New_800TvQ",\
                            u"НовыйДУ800:ALL:ТЗ:Тр:Тр2:t:Значение": "lineEdit_New_800TempBack",\
                            u"НовыйДУ800:ALL:ТЗ:Тр:Тр2:P:Значение": "lineEdit_New_800PressureBack",\
                            u"НовыйДУ800:ALL:ТЗ:Тр:Тр2:Расход:Значение": "lineEdit_New_800FlowBack",\
                            u"НовыйДУ800:ALL:ТЗ:Тр:Тр1:Расход:Значение": "lineEdit_New_800FlowDirect",\
                            u"НовыйДУ800:ALL:ТЗ:Тв:Тв1:M:Значение": "lineEdit_New_800TvM",\

                            u"НовыйЛуговое:ALL:ТЗ:Тр:Тр1:t:Значение": "lineEdit_New_400TempDirect",\
                            u"НовыйЛуговое:ALL:ТЗ:Тр:Тр1:P:Значение": "lineEdit_New_400PressureDirect",\
                            u"НовыйЛуговое:ALL:ТЗ:Тр:Тр1:Расход:Значение": "lineEdit_New_400FlowDirect",\
                            u"НовыйЛуговое:ALL:ТЗ:Тв:Тв1:Q:Значение": "lineEdit_New_400TvQ",\
                            u"НовыйЛуговое:ALL:ТЗ:Тр:Тр2:t:Значение": "lineEdit_New_400TempBack",\
                            u"НовыйЛуговое:ALL:ТЗ:Тр:Тр2:P:Значение": "lineEdit_New_400PressureBack",\
                            u"НовыйЛуговое:ALL:ТЗ:Тр:Тр2:Расход:Значение": "lineEdit_New_400FlowBack",\
                            u"НовыйЛуговое:ALL:ТЗ:Тв:Тв1:M:Значение": "lineEdit_New_400TvM",\

                            u"НовыйТПК-1:ALL:ТЗ:Тр:Тр1:t:Значение": "lineEdit_New_TPK1TempDirect",\
                            u"НовыйТПК-1:ALL:ТЗ:Тр:Тр1:P:Значение": "lineEdit_New_TPK1PressureDirect",\
                            u"НовыйТПК-1:ALL:ТЗ:Тр:Тр1:Расход:Значение": "lineEdit_New_TPK1FlowDirect",\
                            u"НовыйТПК-1:ALL:ТЗ:Тв:Тв1:Q:Значение": "lineEdit_New_TPK1TvQ",\
                            u"НовыйТПК-1:ALL:ТЗ:Тр:Тр2:t:Значение": "lineEdit_New_TPK1TempBack",\
                            u"НовыйТПК-1:ALL:ТЗ:Тр:Тр2:P:Значение": "lineEdit_New_TPK1PressureBack",\
                            u"НовыйТПК-1:ALL:ТЗ:Тр:Тр2:Расход:Значение": "lineEdit_New_TPK1FlowBack",\
                            u"НовыйТПК-1:ALL:ТЗ:Тв:Тв1:M:Значение": "lineEdit_New_TPK1TvM",\

                            u"НовыйТПК-2:ALL:ТЗ:Тр:Тр1:t:Значение": "lineEdit_New_TPK2TempDirect",\
                            u"НовыйТПК-2:ALL:ТЗ:Тр:Тр1:P:Значение": "lineEdit_New_TPK2PressureDirect",\
                            u"НовыйТПК-2:ALL:ТЗ:Тр:Тр1:Расход:Значение": "lineEdit_New_TPK2FlowDirect",\
                            u"НовыйТПК-2:ALL:ТЗ:Тв:Тв1:Q:Значение": "lineEdit_New_TPK2TvQ",\
                            u"НовыйТПК-2:ALL:ТЗ:Тр:Тр2:t:Значение": "lineEdit_New_TPK2TempBack",\
                            u"НовыйТПК-2:ALL:ТЗ:Тр:Тр2:P:Значение": "lineEdit_New_TPK2PressureBack",\
                            u"НовыйТПК-2:ALL:ТЗ:Тр:Тр2:Расход:Значение": "lineEdit_New_TPK2FlowBack",\
                            u"НовыйТПК-2:ALL:ТЗ:Тв:Тв1:M:Значение": "lineEdit_New_TPK2TvM",\

                            # OLD 30:
                            u"ДУ1000:Все переменные:Текущие значения:Трубы:Труба 1:Температура:Значение": "lineEdit_Old_1000TempDirect",\
                            u"ДУ1000:Все переменные:Текущие значения:Трубы:Труба 1:Давление:Значение": "lineEdit_Old_1000PressureDirect",\
                            u"ДУ1000:Все переменные:Текущие значения:Трубы:Труба 1:Расход:Значение": "lineEdit_Old_1000FlowDirect",\
                            u"ДУ1000:Все переменные:Текущие значения:Трубы:Труба 2:Температура:Значение": "lineEdit_Old_1000TempBack",\
                            u"ДУ1000:Все переменные:Текущие значения:Трубы:Труба 2:Давление:Значение": "lineEdit_Old_1000PressureBack",\
                            u"ДУ1000:Все переменные:Текущие значения:Трубы:Труба 2:Расход:Значение": "lineEdit_Old_1000FlowBack",\
                            u"ДУ1000:Все переменные:Текущие значения:Доп.температуры:Tхв:Значение": "lineEdit_Old_1000TvHV",\
                            u"ДУ1000:Все переменные:Текущие значения:Тепловые вводы:Тв1:M:Значение": "lineEdit_Old_1000TvM",\
                            u"ДУ1000:Все переменные:Текущие значения:Тепловые вводы:Тв1:Q:Значение": "lineEdit_Old_1000TvQ",\

                            u"ДУ800:Все переменные:Текущие значения:Трубы:Труба 1:Температура:Значение": "lineEdit_Old_800TempDirect",\
                            u"ДУ800:Все переменные:Текущие значения:Трубы:Труба 1:Давление:Значение": "lineEdit_Old_800PressureDirect",\
                            u"ДУ800:Все переменные:Текущие значения:Трубы:Труба 1:Расход:Значение": "lineEdit_Old_800FlowDirect",\
                            u"ДУ800:Все переменные:Текущие значения:Трубы:Труба 2:Температура:Значение": "lineEdit_Old_800TempTPK2",\
                            u"ДУ800:Все переменные:Текущие значения:Трубы:Труба 2:Давление:Значение": "lineEdit_Old_800PressureTPK2",\
                            u"ДУ800:Все переменные:Текущие значения:Трубы:Труба 2:Расход:Значение": "lineEdit_Old_800FlowTPK2",\
                            u"ДУ800:Все переменные:Текущие значения:Трубы:Труба 3:Температура:Значение": "lineEdit_Old_800TempBack",\
                            u"ДУ800:Все переменные:Текущие значения:Трубы:Труба 3:Давление:Значение": "lineEdit_Old_800PressureBack",\
                            u"ДУ800:Все переменные:Текущие значения:Трубы:Труба 3:Расход:Значение": "lineEdit_Old_800FlowBack",\
                            u"ДУ800:Все переменные:Текущие значения:Доп.температуры:Tхв:Значение": "lineEdit_Old_800TvHV",\
                            u"ДУ800:Все переменные:Текущие значения:Тепловые вводы:Тв1:M:Значение": "lineEdit_Old_800TvM",\
                            u"ДУ800:Все переменные:Текущие значения:Тепловые вводы:Тв1:Q:Значение": "lineEdit_Old_800TvQ",\

                            u"ДУ400:Все переменные:Текущие значения:Трубы:Труба 1:Температура:Значение": "lineEdit_Old_400TempDirect",\
                            u"ДУ400:Все переменные:Текущие значения:Трубы:Труба 1:Давление:Значение": "lineEdit_Old_400PressureDirect",\
                            u"ДУ400:Все переменные:Текущие значения:Трубы:Труба 1:Расход:Значение": "lineEdit_Old_400FlowDirect",\
                            u"ДУ400:Все переменные:Текущие значения:Трубы:Труба 2:Температура:Значение": "lineEdit_Old_400TempBack",\
                            u"ДУ400:Все переменные:Текущие значения:Трубы:Труба 2:Давление:Значение": "lineEdit_Old_400PressureBack",\
                            u"ДУ400:Все переменные:Текущие значения:Трубы:Труба 2:Расход:Значение": "lineEdit_Old_400FlowBack",\
                            u"ДУ400:Все переменные:Текущие значения:Доп.температуры:Tхв:Значение": "lineEdit_Old_400TvHV",\
                            u"ДУ400:Все переменные:Текущие значения:Тепловые вводы:Тв1:M:Значение": "lineEdit_Old_400TvM",\
                            u"ДУ400:Все переменные:Текущие значения:Тепловые вводы:Тв1:Q:Значение": "lineEdit_Old_400TvQ",\

                            # Тр1: СН прямая; Тр2: СН обратная; тр3: подпитка ТС; тр4: ХОВ1; тр5: ХОВ2; тр6: ДСВ400
                            # SN 16:
                            u"СобственныеНужды:ALL:ТЗ:Тр:Тр1:t:Значение": "lineEdit_SN_SNTempDirect",\
                            u"СобственныеНужды:ALL:ТЗ:Тр:Тр1:P:Значение": "lineEdit_SN_SNPressureDirect",\
                            u"СобственныеНужды:ALL:ТЗ:Тр:Тр1:Расход:Значение": "lineEdit_SN_SNFlowDirect",\
                            u"СобственныеНужды:ALL:ТЗ:Тр:Тр2:t:Значение": "lineEdit_SN_SNTempBack",\
                            u"СобственныеНужды:ALL:ТЗ:Тр:Тр2:P:Значение": "lineEdit_SN_SNPressureBack",\
                            u"СобственныеНужды:ALL:ТЗ:Тр:Тр2:Расход:Значение": "lineEdit_SN_SNFlowBack",\
                            u"СобственныеНужды:ALL:ТЗ:Тр:Тр3:t:Значение": "lineEdit_SN_FeedTSTempDirect",\
                            u"СобственныеНужды:ALL:ТЗ:Тр:Тр3:Расход:Значение": "lineEdit_SN_FeedTSFlowDirect",\
                            u"СобственныеНужды:ALL:ТЗ:Тр:Тр4:t:Значение": "lineEdit_SN_HOV1TempDirect",\
                            u"СобственныеНужды:ALL:ТЗ:Тр:Тр4:Расход:Значение": "lineEdit_SN_HOV1FlowDirect",\
                            u"СобственныеНужды:ALL:ТЗ:Тр:Тр5:t:Значение": "lineEdit_SN_HOV2TempDirect",\
                            u"СобственныеНужды:ALL:ТЗ:Тр:Тр5:Расход:Значение": "lineEdit_SN_HOV2FlowDirect",\
                            u"СобственныеНужды:ALL:ТЗ:Тр:Тр6:t:Значение": "lineEdit_SN_DSV400TempDirect",\
                            u"СобственныеНужды:ALL:ТЗ:Тр:Тр6:Расход:Значение": "lineEdit_SN_DSV400FlowDirect",\
                            u"СобственныеНужды:ALL[2]:ТЗ:Тв:Тв1:Q:Значение": "lineEdit_SN_SNQ",\
                            # уровень в баке:
                            u"ДУ400:Все переменные[2]:Текущие значения:Трубы:Труба 3:Давление:Значение": "lineEdit_New_Level"\
                            }

        self.test_dic = {u"ДУ1000:Все переменные:Текущие значения:Трубы:Труба 1:Температура:Значение": "lineEdit_Old_1000TempDirect",\
                            # u"ДУ1000:Все переменные:Архивные часовые значения:Трубы:Труба 1:Температура:Значение": "lineEdit_Old_1000TempDirect",\
                            u"ДУ1000:Все переменные:Текущие значения:Трубы:Труба 1:Давление:Значение": "lineEdit_Old_1000PressureDirect",\
                            u"ДУ1000:Все переменные:Текущие значения:Трубы:Труба 1:Расход:Значение": "lineEdit_Old_1000FlowDirect",\
                            u"ДУ1000:Все переменные:Текущие значения:Трубы:Труба 2:Температура:Значение": "lineEdit_Old_1000TempBack",\
                            u"ДУ1000:Все переменные:Текущие значения:Трубы:Труба 2:Давление:Значение": "lineEdit_Old_1000PressureBack",\
                            u"ДУ1000:Все переменные:Текущие значения:Трубы:Труба 2:Расход:Значение": "lineEdit_Old_1000FlowBack",\
                            u"ДУ1000:Все переменные:Текущие значения:Доп.температуры:Tхв:Значение": "lineEdit_Old_1000TvHV",\
                            u"ДУ1000:Все переменные:Текущие значения:Тепловые вводы:Тв1:M:Значение": "lineEdit_Old_1000TvM",\
                            u"ДУ1000:Все переменные:Текущие значения:Тепловые вводы:Тв1:Q:Значение": "lineEdit_Old_1000TvQ"\
                            }

    def run(self): 
        self.running = True
        print("started teplocom")
        while self.running:
            self.get_prod_teplocom()
        print("stopped teplocom thread")

    def stop(self):
        self.running = False
        print("stop teplocom")

    def get_matrikon(self):
        self.result = list()
        self.matrikon = OpenOPC.client()
        self.matrikon.connect(self.OPC_MATRIKON)
        self.result = self.matrikon.read(self.matrikon_tags)
        self.matrikon.close()
        self.matrikonSignal.emit(self.result)

    def get_teplocom(self):
        self.teplocom = OpenOPC.client()
        # try:
        self.teplocom.connect(self.OPC_TEPLOCOM)
        # except:
        #     print "Не могу подключиться к %s"%self.OPC_TEPLOCOM
        self.result = list()
        # try:
        print "getting tags"
        # self.result = self.teplocom.read(self.teplocom_tags)
        self.result = self.teplocom.read(self.test_dic.keys())
        print "got tags"
        # except:
            # print "нет данных от %s"%self.OPC_TEPLOCOM
        print len(self.result)
        self.teplocom.close()
        # self.teplocomSignal.emit(self.result)
        self.teplocomSignal.emit(self.result)

    def get_prod_teplocom(self):
        self.result = []
        self.teplocom = OpenOPC.client()
        try:
            self.teplocom.connect(self.OPC_TEPLOCOM)
        except:
            print "Не могу подключиться к %s"%self.OPC_TEPLOCOM

        # для прода выбрать prod_dic
        # self.dic = self.test_dic
        self.dic = self.prod_dic
        

        self.tags = self.dic.keys()
        self.result = self.teplocom.read(self.tags)

        for line in self.result:
            name, value, quality, time = line
            print name, value, quality, time
        print "-"*100
            
        # print "нет данных от %s"%self.OPC_TEPLOCOM

        # self.result_dic = dict(zip(self.dic.values(), [line[1] if line[2] == "Good" else 0. for line in self.result]))
        # self.result_dic = dict(zip(self.dic.values(), [ [line[1], line[2]] if line[2] == "Good" else [0., "Bad"] for line in self.result]))
        self.result_dic = dict(zip(self.dic.values(), [ [line[1], line[2]] if line[2] == "Good" else [0., line[2]] for line in self.result]))
        
        # заполняем result_dic нулями, если нет данных от opc для данного lineEdit'a
        for key in self.prod_dic.values():
            self.result_dic[key] = self.result_dic.get(key, [0, "Bad"])
            # self.result_dic[key] = self.result_dic.get(key, [0, random.choice(["Bad", "Good"])]) # тест недостоверности

        # пересчет давлений:
        # self.result_dic["lineEdit_New_1000PressureDirect"] = self.toKgs(self.result_dic["lineEdit_New_1000PressureDirect"])
        # self.result_dic["lineEdit_New_1000PressureBack"] = self.toKgs(self.result_dic["lineEdit_New_1000PressureBack"])
        # self.result_dic["lineEdit_New_800PressureDirect"] = self.toKgs(self.result_dic["lineEdit_New_800PressureDirect"])
        # self.result_dic["lineEdit_New_800PressureBack"] = self.toKgs(self.result_dic["lineEdit_New_800PressureBack"])
        # self.result_dic["lineEdit_New_400PressureDirect"] = self.toKgs(self.result_dic["lineEdit_New_400PressureDirect"])
        # self.result_dic["lineEdit_New_400PressureBack"] = self.toKgs(self.result_dic["lineEdit_New_400PressureBack"])
        # self.result_dic["lineEdit_New_TPK1PressureDirect"] = self.toKgs(self.result_dic["lineEdit_New_TPK1PressureDirect"])
        # self.result_dic["lineEdit_New_TPK1PressureBack"] = self.toKgs(self.result_dic["lineEdit_New_TPK1PressureBack"])
        # self.result_dic["lineEdit_New_TPK2PressureDirect"] = self.toKgs(self.result_dic["lineEdit_New_TPK2PressureDirect"])
        # self.result_dic["lineEdit_New_TPK2PressureBack"] = self.toKgs(self.result_dic["lineEdit_New_TPK2PressureBack"])

        # self.result_dic["lineEdit_Old_1000PressureDirect"] = self.toKgs(self.result_dic["lineEdit_Old_1000PressureDirect"])
        # self.result_dic["lineEdit_Old_1000PressureBack"] = self.toKgs(self.result_dic["lineEdit_Old_1000PressureBack"])
        # self.result_dic["lineEdit_Old_800PressureDirect"] = self.toKgs(self.result_dic["lineEdit_Old_800PressureDirect"])
        # self.result_dic["lineEdit_Old_800PressureBack"] = self.toKgs(self.result_dic["lineEdit_Old_800PressureBack"])
        # self.result_dic["lineEdit_Old_400PressureDirect"] = self.toKgs(self.result_dic["lineEdit_Old_400PressureDirect"])
        # self.result_dic["lineEdit_Old_400PressureBack"] = self.toKgs(self.result_dic["lineEdit_Old_400PressureBack"])

        # self.result_dic["lineEdit_SN_SNPressureDirect"] = self.toKgs(self.result_dic["lineEdit_SN_SNPressureDirect"])
        # self.result_dic["lineEdit_SN_SNPressureBack"] = self.toKgs(self.result_dic["lineEdit_SN_SNPressureBack"])
        
        # пересчет Q:
        self.result_dic["lineEdit_New_1000TvQ"][0] = self.toGcal(self.result_dic["lineEdit_New_1000TvQ"][0])
        self.result_dic["lineEdit_New_800TvQ"][0] = self.toGcal(self.result_dic["lineEdit_New_800TvQ"][0])
        self.result_dic["lineEdit_New_400TvQ"][0] = self.toGcal(self.result_dic["lineEdit_New_400TvQ"][0])
        self.result_dic["lineEdit_New_TPK1TvQ"][0] = self.toGcal(self.result_dic["lineEdit_New_TPK1TvQ"][0])
        self.result_dic["lineEdit_New_TPK2TvQ"][0] = self.toGcal(self.result_dic["lineEdit_New_TPK2TvQ"][0])

        self.result_dic["lineEdit_Old_1000TvQ"][0] = self.toGcal(self.result_dic["lineEdit_Old_1000TvQ"][0])
        self.result_dic["lineEdit_Old_800TvQ"][0] = self.toGcal(self.result_dic["lineEdit_Old_800TvQ"][0])
        self.result_dic["lineEdit_Old_400TvQ"][0] = self.toGcal(self.result_dic["lineEdit_Old_400TvQ"][0])

        self.result_dic["lineEdit_SN_SNQ"][0] = self.toGcal(self.result_dic["lineEdit_SN_SNQ"][0])
        
        # counting all mass differences (feeds) and totals (M direct, M back, Feed, Q):
        # OLD:
        Old_1000Feed = self.result_dic.get("lineEdit_Old_1000FlowDirect", [0., "Bad"])[0] -\
                       self.result_dic.get("lineEdit_Old_1000FlowBack", [0., "Bad"])[0]
        self.result_dic["lineEdit_Old_1000Feed"] = [Old_1000Feed, "Good"]

        Old_800Feed = self.result_dic.get("lineEdit_Old_800FlowDirect", [0., "Bad"])[0] +\
                      self.result_dic.get("lineEdit_Old_800FlowTPK2", [0., "Bad"])[0] -\
                      self.result_dic.get("lineEdit_Old_800FlowBack", [0., "Bad"])[0]
        self.result_dic["lineEdit_Old_800Feed"] = [Old_800Feed, "Good"]
        
        Old_400Feed = self.result_dic.get("lineEdit_Old_400FlowDirect", [0., "Bad"])[0] -\
                      self.result_dic.get("lineEdit_Old_400FlowBack", [0., "Bad"])[0]
        self.result_dic["lineEdit_Old_400Feed"] = [Old_400Feed, "Good"]
        
        Old_TotalMassDirect = self.result_dic.get("lineEdit_Old_1000FlowDirect", [0., "Bad"])[0] +\
                              self.result_dic.get("lineEdit_Old_800FlowDirect", [0., "Bad"])[0] +\
                              self.result_dic.get("lineEdit_Old_400FlowDirect", [0., "Bad"])[0]
        self.result_dic["lineEdit_Old_TotalMDirect"] = [Old_TotalMassDirect, "Good"]

        Old_TotalMassBack = self.result_dic.get("lineEdit_Old_1000FlowBack", [0., "Bad"])[0] +\
                            self.result_dic.get("lineEdit_Old_800FlowBack", [0., "Bad"])[0] +\
                            self.result_dic.get("lineEdit_Old_400FlowBack", [0., "Bad"])[0]
        self.result_dic["lineEdit_Old_TotalMBack"] = [Old_TotalMassBack, "Good"]

        Old_TotalFeed = self.result_dic.get("lineEdit_Old_1000TvM", [0., "Bad"])[0] +\
                        self.result_dic.get("lineEdit_Old_800TvM", [0., "Bad"])[0] +\
                        self.result_dic.get("lineEdit_Old_400TvM", [0., "Bad"])[0]
        self.result_dic["lineEdit_Old_TotalFeed"] = [Old_TotalFeed, "Good"]
        
        Old_TotalQ = self.result_dic.get("lineEdit_Old_1000TvQ", [0., "Bad"])[0] +\
                     self.result_dic.get("lineEdit_Old_800TvQ", [0., "Bad"])[0] +\
                     self.result_dic.get("lineEdit_Old_400TvQ", [0., "Bad"])[0]
        self.result_dic["lineEdit_Old_TotalQ"] = [Old_TotalQ, "Good"]

        # NEW:
        # Feeds
        New_1000Feed = self.result_dic.get("lineEdit_New_1000FlowDirect", [0., "Bad"])[0] -\
                       self.result_dic.get("lineEdit_New_1000FlowBack", [0., "Bad"])[0]
        self.result_dic["lineEdit_New_1000Feed"] = [New_1000Feed, "Good"]

        New_800Feed = self.result_dic.get("lineEdit_New_800FlowDirect", [0., "Bad"])[0] -\
                      self.result_dic.get("lineEdit_New_800FlowBack", [0., "Bad"])[0]
        self.result_dic["lineEdit_New_800Feed"] = [New_800Feed, "Good"]
        
        New_400Feed = self.result_dic.get("lineEdit_New_400FlowDirect", [0., "Bad"])[0] -\
                      self.result_dic.get("lineEdit_New_400FlowBack", [0., "Bad"])[0]
        self.result_dic["lineEdit_New_400Feed"] = [New_400Feed, "Good"]

        New_TPK1Feed = self.result_dic.get("lineEdit_New_TPK1FlowDirect", [0., "Bad"])[0] -\
                       self.result_dic.get("lineEdit_New_TPK1FlowBack", [0., "Bad"])[0]
        self.result_dic["lineEdit_New_TPK1Feed"] = [New_TPK1Feed, "Good"]

        New_TPK2Feed = self.result_dic.get("lineEdit_New_TPK2FlowDirect", [0., "Bad"])[0] -\
                       self.result_dic.get("lineEdit_New_TPK2FlowBack", [0., "Bad"])[0]
        self.result_dic["lineEdit_New_TPK2Feed"] = [New_TPK2Feed, "Good"]
        # Totals
        New_TotalFlowDirect = self.result_dic.get("lineEdit_New_1000FlowDirect", [0., "Bad"])[0] +\
                              self.result_dic.get("lineEdit_New_800FlowDirect", [0., "Bad"])[0] +\
                              self.result_dic.get("lineEdit_New_400FlowDirect", [0., "Bad"])[0] +\
                              self.result_dic.get("lineEdit_New_TPK1FlowDirect", [0., "Bad"])[0] +\
                              self.result_dic.get("lineEdit_New_TPK2FlowDirect", [0., "Bad"])[0]
        self.result_dic["lineEdit_New_TotalFlowDirect"] = [New_TotalFlowDirect, "Good"]

        New_TotalFlowBack = self.result_dic.get("lineEdit_New_1000FlowBack", [0., "Bad"])[0] +\
                            self.result_dic.get("lineEdit_New_800FlowBack", [0., "Bad"])[0] +\
                            self.result_dic.get("lineEdit_New_400FlowBack", [0., "Bad"])[0] +\
                            self.result_dic.get("lineEdit_New_TPK1FlowBack", [0., "Bad"])[0] +\
                            self.result_dic.get("lineEdit_New_TPK2FlowBack", [0., "Bad"])[0]
        self.result_dic["lineEdit_New_TotalFlowBack"] = [New_TotalFlowBack, "Good"]

        New_TotalFeed = self.result_dic.get("lineEdit_New_TotalFlowDirect", [0., "Bad"])[0] -\
                        self.result_dic.get("lineEdit_New_TotalFlowBack", [0., "Bad"])[0]
        self.result_dic["lineEdit_New_TotalFeed"] = [New_TotalFeed, "Good"]

        New_TotalMass = self.result_dic.get("lineEdit_New_1000TvM", [0., "Bad"])[0] +\
                        self.result_dic.get("lineEdit_New_800TvM", [0., "Bad"])[0] +\
                        self.result_dic.get("lineEdit_New_400TvM", [0., "Bad"])[0] +\
                        self.result_dic.get("lineEdit_New_TPK1TvM", [0., "Bad"])[0] +\
                        self.result_dic.get("lineEdit_New_TPK2TvM", [0., "Bad"])[0]
        self.result_dic["lineEdit_New_TotalTvM"] = [New_TotalMass, "Good"]
        
        New_TotalQ = self.result_dic.get("lineEdit_New_1000TvQ", [0., "Bad"])[0] +\
                     self.result_dic.get("lineEdit_New_800TvQ", [0., "Bad"])[0] +\
                     self.result_dic.get("lineEdit_New_400TvQ", [0., "Bad"])[0] +\
                     self.result_dic.get("lineEdit_New_TPK1TvQ", [0., "Bad"])[0] +\
                     self.result_dic.get("lineEdit_New_TPK2TvQ", [0., "Bad"])[0]
        self.result_dic["lineEdit_New_TotalTvQ"] = [New_TotalQ, "Good"]

        # SN:
        SN_SNdM = self.result_dic.get("lineEdit_SN_SNFlowDirect", [0., "Bad"])[0] -\
                  self.result_dic.get("lineEdit_SN_SNFlowBack", [0., "Bad"])[0]
        self.result_dic["lineEdit_SN_SNFlowDM"] = [SN_SNdM, "Good"]

        SN_FeedTSFlowDM = self.result_dic.get("lineEdit_SN_FeedTSFlowDirect", [0., "Bad"])[0] -\
                          self.result_dic.get("lineEdit_SN_DSV400FlowDirect", [0., "Bad"])[0]
        self.result_dic["lineEdit_SN_FeedTSFlowDM"] = [SN_FeedTSFlowDM, "Good"]

        SN_HOV2FlowDM = self.result_dic.get("lineEdit_SN_HOV1FlowDirect", [0., "Bad"])[0] +\
                        self.result_dic.get("lineEdit_SN_HOV2FlowDirect", [0., "Bad"])[0]
        self.result_dic["lineEdit_SN_HOV2FlowDM"] = [SN_HOV2FlowDM, "Good"]

        SN_SNTempDT = self.result_dic.get("lineEdit_SN_SNTempDirect", [0., "Bad"])[0] -\
                      self.result_dic.get("lineEdit_SN_SNTempBack", [0., "Bad"])[0]
        self.result_dic["lineEdit_SN_SNTempDT"] = [SN_SNTempDT, "Good"]

        SN_SNPressureDP = self.result_dic.get("lineEdit_SN_SNPressureDirect", [0., "Bad"])[0] -\
                          self.result_dic.get("lineEdit_SN_SNPressureBack", [0., "Bad"])[0]
        self.result_dic["lineEdit_SN_SNPressureDP"] = [SN_SNPressureDP, "Good"]

        self.result_dic["lineEdit_Old_Level"] = self.result_dic["lineEdit_New_Level"]



        for key, value in self.result_dic.items():
            # print key, value
            self.query = "INSERT INTO vkt_data (name, quality, value, timestamp, test, scheme, report_order)\
                VALUES ('%s','Good','%s','%s','%s', '%s', '%s');"%(key, value[0], datetime.datetime.now(), 0,\
                    key.split("_")[1].lower()+"_", self.report_order[key])
            self.write_task = WriteTask(self.query)
            self.queue.put(self.write_task)

        self.teplocom.close()
        self.teplocomprodSignal.emit(self.result_dic)


    def toKgs(self, pressure):
        return pressure*9.8

    def toGcal(self, q):
        return float(q)/4.184
    
class WriteTask(QtCore.QObject):
    def __init__(self, sql):
        super(WriteTask, self).__init__()
        self.sql = sql

    def run(self):
        self.connection = sqlite3.connect("vkt.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.sql)
        self.connection.commit()
        self.cursor.close()





if __name__ == "__main__":
    c = OpcThread(Queue.Queue())
    c.get_prod_teplocom()

    print c.queue.qsize()

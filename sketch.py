# coding: utf-8
import OpenOPC
OPC_TEPLOCOM = "InSAT.OPC.Teplocom.Da"

test_dic = {u"ДУ1000:Все переменные:Текущие значения:Трубы:Труба 1:Температура:Значение": "lineEdit_Old_1000TempDirect",\

                             u"ДУ800:Все переменные:Текущие значения:Тепловые вводы:Тв1:Q:Значение": "lineEdit_Old_800TvQ",\

                            u"ДУ400:Все переменные:Текущие значения:Трубы:Труба 1:Температура:Значение": "lineEdit_Old_400TempDirect",\
                            # u"СобственныеНужды:ALL:ТЗ:Тр:Тр1:t:Значение": "lineEdit_SN_SNTempDirect",\
                            # u"СобственныеНужды:ALL:ТЗ:Тр:Тр1:P:Значение": "lineEdit_SN_SNPressureDirect",\
                            # u"СобственныеНужды:ALL:ТЗ:Тр:Тр1:Расход:Значение": "lineEdit_SN_SNFlowDirect",\
                            # u"СобственныеНужды:ALL:ТЗ:Тр:Тр2:t:Значение": "lineEdit_SN_SNTempBack",\
                            # u"СобственныеНужды:ALL:ТЗ:Тр:Тр2:P:Значение": "lineEdit_SN_SNPressureBack",\
                            # u"СобственныеНужды:ALL:ТЗ:Тр:Тр2:Расход:Значение": "lineEdit_SN_SNFlowBack",\
                            # u"СобственныеНужды:ALL:ТЗ:Тр:Тр3:t:Значение": "lineEdit_SN_FeedTSTempDirect",\
                            # u"СобственныеНужды:ALL:ТЗ:Тр:Тр3:Расход:Значение": "lineEdit_SN_FeedTSFlowDirect",\
                            # u"СобственныеНужды:ALL:ТЗ:Тр:Тр4:t:Значение": "lineEdit_SN_HOV1TempDirect",\
                            # u"СобственныеНужды:ALL:ТЗ:Тр:Тр4:Расход:Значение": "lineEdit_SN_HOV1FlowDirect",\
                            # u"СобственныеНужды:ALL:ТЗ:Тр:Тр5:t:Значение": "lineEdit_SN_HOV2TempDirect",\
                            # u"СобственныеНужды:ALL:ТЗ:Тр:Тр5:Расход:Значение": "lineEdit_SN_HOV2FlowDirect",\
                            # u"СобственныеНужды:ALL:ТЗ:Тр:Тр6:t:Значение": "lineEdit_SN_DSV400TempDirect",\
                            # u"СобственныеНужды:ALL:ТЗ:Тр:Тр6:Расход:Значение": "lineEdit_SN_DSV400FlowDirect",\
                            u"СобственныеНужды:ALL[2]:ТЗ:Тв:Тв1:Q:Значение": "lineEdit_SN_SNQ",\
                            # уровень в баке:
                            u"ДУ400:Все переменные[2]:Текущие значения:Трубы:Труба 3:Давление:Значение": "lineEdit_New_Level"\
                            }

teplocom = OpenOPC.client()
teplocom.connect(OPC_TEPLOCOM)
result = teplocom.read(test_dic.keys())
print result
from parse_mopc import OpcTree

prefix = {"new": "New_", "old": "Old_", "sn": "SN_"}
pipes = ["1000", "800", "400", "TPK1", "TPK2"]
directions = ["Direct", "Back"]
parameters = ["Temp", "Pressure", "Flow"]
MQ = ["M", "Q"]
MQT = ["M", "Q", "HV"]





def lineEdits(prefix, pipes, directions, parameters, mqt):


    lineEdits = ["lineEdit_" + prefix + pipe + par + d for pipe in pipes for par in parameters\
                            for d in directions]

    feeds = ["lineEdit_" + prefix + pipe + "Feed" for pipe in pipes  ]

    lineEdits += feeds

    tvs = ["lineEdit_" + prefix + pipe + "Tv" + mq for pipe in pipes for mq in mqt ]
    lineEdits += tvs

    return lineEdits

new_lineEdits = lineEdits(prefix["new"], pipes, directions , parameters, MQ)
new_TotallineEdits = ["lineEdit_New_TotalFlowDirect", "lineEdit_New_TotalFlowBack",\
                    "lineEdit_New_TotalFeed", "lineEdit_New_TotalTvM", "lineEdit_New_TotalTvQ"]

old_lineEdits = lineEdits(prefix["old"], pipes[:3], directions, parameters, MQT)
old_TotallineEdits = ["lineEdit_Old_TotalMDirect", "lineEdit_Old_TotalMBack", "lineEdit_Old_TotalQ",\
                    "lineEdit_Old_TotalFeed"]

sn_lineEdits  = ["lineEdit_SN_SNFlowDirect", "lineEdit_SN_SNFlowBack", "lineEdit_SN_SNFlowDM",\
                 "lineEdit_SN_SNTempDirect", "lineEdit_SN_SNTempBack", "lineEdit_SN_SNTempDT",\
                 "lineEdit_SN_SNPressureDirect", "lineEdit_SN_SNPressureBack", "lineEdit_SN_SNPressureDP",\
                 "lineEdit_SN_SNQ",\
                 "lineEdit_SN_FeedTSFlowDirect", "lineEdit_SN_FeedTSTempDirect", "lineEdit_SN_FeedTSFlowDM",\
                 "lineEdit_SN_DSV400FlowDirect", "lineEdit_SN_DSV400TempDirect",\
                 "lineEdit_SN_HOV1FlowDirect", "lineEdit_SN_HOV1TempDirect",\
                 "lineEdit_SN_HOV2FlowDirect", "lineEdit_SN_HOV2TempDirect", "lineEdit_SN_HOV2FlowDM"]

all_lineEdits = new_lineEdits + old_lineEdits + sn_lineEdits



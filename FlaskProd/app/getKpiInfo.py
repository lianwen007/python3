from flask import Blueprint, render_template, redirect,request
from app import app
from .relog import log
#from .models import Stwdaycount
import json,time,requests,uuid
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

getKpiInfo = Blueprint('getKpiInfo',__name__)

@getKpiInfo.route('/bigdata/product_stw/getkpiinfo', methods=['GET'])
def get_kpiinfo():
    schoolid = str(request.values.get('schoolId'))
    starttime = request.values.get('startTime',int(time.time()) - 24*60*60*8)
    endedtime = request.values.get('endTime',int(time.time()))
    traceId = str(uuid.uuid1()).replace('-', '')
    s = Getkpiinfo(schoolid, starttime, endedtime,traceId)
    return json.dumps(s.main(), ensure_ascii=False)

class Getkpiinfo(object):
    def __init__(self, schoolid, starttime, endedtime, traceId):
        self.schoolid = schoolid
        self.starttime = starttime
        self.endedtime = endedtime
        self.checkscid = ''
        self.traceId = traceId

    def checkschoolid(self):
        sql = "select distinct schoolid from product_stw_daycount where schoolid in (%s) \
                and (unix_timestamp(`datetime`)>=%s and unix_timestamp(`datetime`)<=%s)" % (
        self.schoolid, self.starttime, self.endedtime)
        rs = db.session.execute(sql)
        if len([chrs for chrs in rs ])>0:
            self.checkscid = 'right'

    def getkpiinfo(self):
        descnames = ['userid', 'username', 'schoolid', 'schoolname', 'classname', 'classid',
                     'bookname', 'bookid', 'hp', 'credit', 'countscore', 'numhomework', 'numselfwork',
                     'topicnum', 'countright', 'rightlv', 'counttime', 'datetime']

        sqlsel = "select * from product_stw_daycount where schoolid in (%s) \
            and (unix_timestamp(`datetime`)>=%s and unix_timestamp(`datetime`)<=%s) \
            order by `datetime` DESC " % (self.schoolid, self.starttime, self.endedtime)
        data_list  = db.session.execute(sqlsel)
        messes, mesind, finad = [], [], []
        for datas in data_list:
            mess = {}
            for x in range(len(datas)):
                mess[descnames[x]] = datas[x]
            messes.append(mess)
        for mes in messes:
            mesind.append(mes['userid'])
        mesindex = list(set(mesind))
        zdatas=messes
        for y in mesindex:
            # findata=[]
            dataz = []
            for mes in zdatas:
                if mes['userid'] == y:
                    dataz.append(mes)
            # findata.append(dataz)
            finad.append(dataz)
        return finad
    def main(self):
        Getkpiinfo.checkschoolid(self)
        data = {}
        data['traceId'] = self.traceId
        if self.checkscid == 'right':
            data['code'] = 200
            data['data'] = Getkpiinfo.getkpiinfo(self)
            data['msg'] = 'successful!'
        else:
            data['code'] = 400
            data['msg'] = 'These schools is not exist!'
        logInfo = str(data['code'])  + '[' + self.traceId + ']type[getStwinfo]' + 'scid[' + self.schoolid + ']'\
                  + 'sttime[' + str(self.starttime) + ']' + 'endtime[' + str(self.endedtime) + ']'
        log('APIRequest-', logInfo)
        return data

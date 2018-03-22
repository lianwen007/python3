from flask import Blueprint, render_template, redirect,request,jsonify
from app import app
from .relog import log
#from .models import Stwdaycount
import json,time,requests
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

getKpiInfo = Blueprint('getKpiInfo',__name__)
def getTraceId():
    import uuid
    return str(uuid.uuid1()).replace('-', '')

@getKpiInfo.route('/bigdata/product_stw/subject/<int:subjectId>/getKpiInfo', methods=['GET'])
def get_kpiinfo(subjectId):
    schoolid = request.values.get('schoolId')
    starttime = request.values.get('startTime', int(time.time()) - 24*60*60*8)
    endedtime = request.values.get('endTime', int(time.time()))
    if not schoolid:
        mess ={'code':400,'mess': 'Error! Please enter the correct schoolId!',}
        logInfo = '400' + '[' + getTraceId() + ']type[getKpiInfo]' + 'scid[Noid]subjectid[' \
                  + str(subjectId) + ']sttime[' + str(starttime) + ']endtime[' + str(endedtime) + ']'
        log('APIRequest-', logInfo)
        return jsonify(mess)
    else:
        s = Getkpiinfo(schoolid, starttime, endedtime, subjectId)
        return jsonify(s.main())

class Getkpiinfo(object):
    def __init__(self, schoolid, starttime, endedtime, subjectId):
        self.schoolid = schoolid
        self.starttime = starttime
        self.endedtime = endedtime
        self.subjectid = subjectId
        self.checkscid = ''

    def checkschoolid(self):
        sql = "select distinct schoolid from product_stw_kpicount where schoolid in (%s) \
                and (unix_timestamp(`datetime`)>=%s and unix_timestamp(`datetime`)<=%s)" % (
        self.schoolid, self.starttime, self.endedtime)
        rs = db.session.execute(sql)
        if len([chrs for chrs in rs ])>0:
            self.checkscid = 'right'

    def getkpiinfo(self):
        descnames = ['tchId', 'tchName', 'classId', 'className', 'stuNum', 'practiceNum', 'taskFixNum', 'taskStuNum', 'taskUploadNum']
        sqlsel = "SELECT teacherid,teachername,classid,classname,studentnum,CAST(SUM(practicenum)AS SIGNED) practiceNum,CAST(SUM(taskfixnum)AS SIGNED)taskFixNum,\
            CAST(SUM(taskstunum)AS SIGNED)taskStuNum,CAST(SUM(taskupnum)AS SIGNED)taskUploadNum FROM product_stw_kpicount WHERE schoolid=%s \
            AND subjectid=%s AND (`datetime`>=FROM_UNIXTIME(%s,'%%Y%%m%%d') AND `datetime`<=FROM_UNIXTIME(%s,'%%Y%%m%%d'))\
            GROUP BY teacherid,teachername,classid,classname,studentnum" % (self.schoolid, self.subjectid, self.starttime, self.endedtime)
        data_list = db.session.execute(sqlsel)
        messes = []
        for datas in data_list:
            mess = {}
            for x in range(len(datas)):
                mess[descnames[x]] = datas[x]
            messes.append(mess)
        return messes

    def main(self):
        data = {}
        data['traceId'] = getTraceId()
        self.checkschoolid()
        if self.checkscid == 'right':
            data['code'] = 200
            data['data'] = self.getkpiinfo()
            data['msg'] = 'successful!'
        else:
            data['code'] = 400
            data['msg'] = 'Error! These schools are not exist!'
        logInfo = str(data['code'])  + '[' + data['traceId'] + ']type[getKpiInfo]' + 'scid[' + str(self.schoolid) + ']subjectid['\
                  + str(self.subjectid) + ']sttime[' + str(self.starttime) + ']endtime[' + str(self.endedtime) + ']'
        log('APIRequest-', logInfo)
        return data

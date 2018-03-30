from flask import Blueprint, render_template, redirect,request,jsonify
from app import app,cache
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
        traceid=getTraceId()
        mess ={'code':400,'msg': 'Error! Please enter the correct schoolId!','traceId':traceid}
        logInfo = '400' + '[' + traceid + ']type[getKpiInfo]' + 'scid[Noid]subjectid[' \
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
        @cache.memoize(timeout=3600*12)
        def get_teacher_subject(schoolId, subjectId):
            # 调取业务实时数据接口，取得数据
            url = 'http://admin.yunzuoye.net/api/user/subjectTch'
            # url = 'http://bigdata.yunzuoye.net/student/studentInfo'
            getdata = {"schoolId": schoolId, "subjectId": subjectId, }
            try:
                reqdatas = requests.get(url, params=getdata, timeout=2).json()
            except:
                reqdatas = []
            return reqdatas

        descnames = ['tchId', 'tchName', 'classId', 'className', 'stuNum', 'practiceNum', 'taskFixNum', 'taskStuNum', 'taskUploadNum']
        sqlsel = "SELECT teacherid,teachername,classid,classname,studentnum,CAST(SUM(practicenum)AS SIGNED) practiceNum,CAST(SUM(taskfixnum)AS SIGNED)taskFixNum,\
            CAST(SUM(taskstunum)AS SIGNED)taskStuNum,CAST(SUM(taskupnum)AS SIGNED)taskUploadNum FROM product_stw_kpicount WHERE schoolid=%s \
            AND subjectid=%s AND (`datetime`>=FROM_UNIXTIME(%s,'%%Y%%m%%d') AND `datetime`<=FROM_UNIXTIME(%s,'%%Y%%m%%d'))\
            GROUP BY teacherid,teachername,classid,classname,studentnum" % (self.schoolid, self.subjectid, self.starttime, self.endedtime)
        data_list = db.session.execute(sqlsel)
        messes = []
        reqteachers = get_teacher_subject(self.schoolid, self.subjectid)
        for datas in data_list:
            mess = {}
            for x in range(len(datas)):
                mess[descnames[x]] = datas[x]
            messes.append(mess)
        finalData = []
        if reqteachers:
            for messfin in messes:
                for reqteacher in reqteachers:
                    if str(messfin['tchId']) == str(reqteacher['userId']):
                        finalData.append(messfin)
        else:
            finalData = messes
        return finalData

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

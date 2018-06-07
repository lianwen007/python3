from flask import Blueprint, render_template, redirect,request,jsonify
from app import app,cache
from .relog import log
#from .models import Stwdaycount
import json,time,requests
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

getKpiInfo = Blueprint('getKpiInfo', __name__)


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


@getKpiInfo.route('/bigdata/product_stw/subject/clearCache', methods=['GET'])
def subject_cache_clear():
    password = request.values.get('password')
    if password == 'bigdata123':
        cache.clear()
        datas = {'msg':'Successful! Clear All'}
    else:
        datas = {'msg':'Error, Password was wrong!'}
    return jsonify(datas)


class Getkpiinfo(object):
    def __init__(self, schoolid, starttime, endedtime, subjectId):
        self.schoolid = schoolid
        self.starttime = starttime
        self.endedtime = endedtime
        self.subjectid = subjectId
        self.checkscid = ''

    def checkschoolid(self):
        sql = "select distinct schoolid from teacher_info_stunum where schoolid in (%s)" % self.schoolid
        rs = db.session.execute(sql)
        if len([chars for chars in rs]) > 0:
            self.checkscid = 'right'

    def get_all_teacher(self):
        # 获取学校对应的老师班级
        @cache.memoize(timeout=3600*8)  # 设置缓存8小时
        def get_all_user_cache(school_id):
            names = ['tchId', 'tchName', 'classId', 'className', 'stuNum']
            sql = "SELECT DISTINCT teacherid,teachername,classid,classname,studentnum FROM teacher_info_stunum " \
                  "WHERE schoolid IN (%s)" % school_id
            try:
                data_lists = db.session.execute(sql)
            except Exception as e:
                log('Error[getQstNum]-[get_all_user]', e)
                data_lists = list()
            messes = list()
            for data in data_lists:
                mess = dict()
                for x in range(len(data)):
                    mess[names[x]] = data[x]
                messes.append(mess)
            return messes
        return get_all_user_cache(self.schoolid)

    def getkpiinfo(self):
        @cache.memoize(timeout=3600*12)
        def get_teacher_subject(schoolId, subjectId):
            # 调取业务实时数据接口，取得数据
            subpart = {1:"语文", 2:"数学", 3:"英语", 4:"科学", 5:"历史", 6:"道德与法治", 7:"物理", }
            url = 'http://admin.yunzuoye.net/api/user/subjectTch'
            getdata = {"schoolId": schoolId, "subjectName": subpart.get(subjectId)}
            try:
                reqdatas = requests.get(url, params=getdata, timeout=2).json()
            except:
                reqdatas = []
                #cache.delete_memoized('get_teacher_subject', schoolId, subjectId)
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
        all_teachers = self.get_all_teacher()
        values = list()
        for all_teacher in all_teachers:
            all_teacher['practiceNum'] = 0
            all_teacher['taskFixNum'] = 0
            all_teacher['taskStuNum'] = 0
            all_teacher['taskUploadNum'] = 0
            for m in messes:
                if str(all_teacher['tchId']) == str(m['tchId']) and str(all_teacher['classId']) == str(m['classId']):
                    all_teacher['practiceNum'] = m['practiceNum']
                    all_teacher['taskFixNum'] = m['taskFixNum']
                    all_teacher['taskStuNum'] = m['taskStuNum']
                    all_teacher['taskUploadNum'] = m['taskUploadNum']
            values.append(all_teacher)
        finalData = []
        if reqteachers:
            for messfin in values:
                for reqteacher in reqteachers:
                    if str(messfin['tchId']) == str(reqteacher['userId']):
                        finalData.append(messfin)
        else:
            finalData = values
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
        logInfo = str(data['code']) + '[' + data['traceId'] + ']type[getKpiInfo]' + 'scid[' + str(self.schoolid) + \
                  ']subjectid[' + str(self.subjectid) + ']sttime[' + str(self.starttime) + ']endtime[' + str(self.endedtime) + ']'
        log('APIRequest-', logInfo)
        return data

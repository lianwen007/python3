from flask import Blueprint, render_template, redirect,request,jsonify
from app import app,cache
from .relog import log
#from .models import Stwdaycount
import json,time,requests
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

getEnStwInfo = Blueprint('getEnStwInfo', __name__)
def getTraceId():
    import uuid
    return str(uuid.uuid1()).replace('-', '')

@getEnStwInfo.route('/bigdata/product_stw/enstwInfo/getEnStwInfo', methods=['GET'])
def get_enstw_info():
    schoolid = request.values.get('schoolId')
    starttime = request.values.get('startTime', int(time.time()) - 24*60*60*8)
    endedtime = request.values.get('endTime', int(time.time()))
    if not schoolid:
        traceid=getTraceId()
        mess ={'code': 400, 'msg': 'Error! Please enter the correct schoolId!', 'traceId': traceid}
        logInfo = '400' + '[' + traceid + ']type[getEnStwInfo]' + 'scid[Noid]' \
                  +'sttime[' + str(starttime) + ']endtime[' + str(endedtime) + ']'
        log('APIRequest-', logInfo)
        return jsonify(mess)
    else:
        s = GetEnStwInfo(schoolid, starttime, endedtime,)
        return jsonify(s.main())

@getEnStwInfo.route('/bigdata/product_stw/enstwInfo/clearCache', methods=['GET'])
def enstw_cache_clear():
    password = request.values.get('password')
    if password == 'bigdata123':
        cache.clear()
        datas = {'msg': 'Successful! Clear All'}
    else:
        datas = {'msg': 'Error, Password was wrong!'}
    return jsonify(datas)

class GetEnStwInfo(object):
    def __init__(self, schoolid, starttime, endedtime,):
        self.schoolid = schoolid
        self.starttime = starttime
        self.endedtime = endedtime
        self.checkscid = ''
        self.alldescs = ['userId', 'userName', 'schoolId', 'classId', 'className']

    def check_school_id(self):
        sql = "select distinct schoolid from product_stw_encount where schoolid in (%s) \
                and (unix_timestamp(`datetime`)>=%s and unix_timestamp(`datetime`)<=%s)" % (
        self.schoolid, self.starttime, self.endedtime)
        rs = db.session.execute(sql)
        if len([chrs for chrs in rs ])>0:
            self.checkscid = 'right'

    def get_enstw_info(self):
        @cache.memoize(timeout=3600 * 12)
        def get_all_user(schoolid, alldescs):
            # 获取学校的所有学生列表
            sqlsel = "select DISTINCT userid,username,schoolid,classid,classname from teacher_student_info  " \
                     "where classname!='教师' AND schoolid in (%s)" % (schoolid)
            data_lists = db.session.execute(sqlsel)
            messes = []
            for datas in data_lists:
                mess = {}
                for x in range(len(datas)):
                    mess[alldescs[x]] = datas[x]
                messes.append(mess)
            return messes

        descnames = ['userId', 'userName', 'schoolId', 'classId', 'className', 'gameCount', 'finCount',
                     'homeFull', 'selfCount', 'selfFull', 'listenNum', 'readNum', 'blankNum']
        sqlsel = "SELECT userid,username,schoolid,classid,classname,CAST(SUM(gamecount)AS SIGNED),CAST(SUM(finishcount)AS SIGNED),\
                CAST(SUM(homefull)AS SIGNED),CAST(SUM(selfcount)AS SIGNED),CAST(SUM(selffull)AS SIGNED),CAST(SUM(listennum)AS SIGNED),\
                 CAST(SUM(readnum)AS SIGNED),CAST(SUM(blanknum)AS SIGNED) FROM product_stw_encount WHERE schoolid=%s \
                  AND unix_timestamp(`datetime`)>=%s AND unix_timestamp(`datetime`)<=%s GROUP BY userid,username,schoolid,classid,classname" \
                 % (self.schoolid, self.starttime, self.endedtime)
        data_list = db.session.execute(sqlsel)
        messes = []
        for datas in data_list:
            mess = {}
            for x in range(len(datas)):
                mess[descnames[x]] = datas[x]
            messes.append(mess)
        student_all=get_all_user(self.schoolid,self.alldescs)
        alldatas = []
        for allmess in student_all:
            for rdataf in messes:
                if int(rdataf["userId"]) == int(allmess["userId"]):
                    for finone in descnames[5:]:
                        allmess[finone] = rdataf[finone]
            if len(allmess) == len(self.alldescs):
                 for findena in descnames[5:]:
                     allmess[findena] = 0
            alldatas.append(allmess)

        return alldatas

    def main(self):
        data = { }
        data['traceId'] = getTraceId()
        self.check_school_id()
        if self.checkscid == 'right':
            data['code'] = 200
            data['data'] = self.get_enstw_info()
            data['msg'] = 'successful!'
        else:
            data['code'] = 400
            data['msg'] = 'Error! These schools are not exist!'
        logInfo = str(data['code'])  + '[' + data['traceId'] + ']type[getEnStwInfo]' + 'scid[' + str(self.schoolid) \
                   + ']sttime[' + str(self.starttime) + ']endtime[' + str(self.endedtime) + ']'
        log('APIRequest-', logInfo)
        return data

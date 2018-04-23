from flask import Blueprint, render_template, redirect,request,jsonify
from app import app, cache
from .relog import log
#from .models import Stwdaycount
import json,time,requests
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
getEnStwInfo = Blueprint('getEnStwInfo', __name__)


def getTraceId():
    import uuid
    return str(uuid.uuid1()).replace('-', '')


def keep_percent_point_num(num, point):
    # 小数化为百分比，并保留小数位数
    return int(num*10**(point+2))/10**point


@getEnStwInfo.route('/getEnStwInfo', methods=['GET'])
def get_enstw_info():
    schoolid = request.values.get('schoolId')
    classid = request.values.get('classId', '0')
    starttime = request.values.get('startTime', int(time.time()) - 24*60*60*8)
    endedtime = request.values.get('endTime', int(time.time()))
    if not schoolid:
        traceid=getTraceId()
        mess = {'code': 400, 'msg': 'Error! Please enter the correct schoolId!', 'traceId': traceid}
        logInfo = '400' + '[' + traceid + ']type[getEnStwInfo]' + 'scid[Noid]clid[Noid]' \
                  +'sttime[' + str(starttime) + ']endtime[' + str(endedtime) + ']'
        log('APIRequest-', logInfo)
        return jsonify(mess)
    else:
        s = GetEnStwInfo(schoolid, classid, starttime, endedtime,)
        return jsonify(s.main())


@getEnStwInfo.route('/clearCache', methods=['GET'])
def enstw_cache_clear():
    password = request.values.get('password')
    if password == 'bigdata123':
        cache.clear()
        datas = {'msg': 'Succeed to clear all'}
    else:
        datas = {'msg': 'Error, Password was wrong!'}
    return jsonify(datas)

class GetEnStwInfo(object):
    def __init__(self, schoolid, classid, starttime, endedtime,):
        self.schoolid = schoolid
        self.starttime = starttime
        self.endedtime = endedtime
        self.classid = classid
        self.checkscid = ''
        self.alldescs = ['userId', 'userName', 'schoolId', 'classId', 'className']

    def check_school_id(self):
        sql = "select distinct schoolid from product_stw_encount where schoolid in (%s) \
                and (unix_timestamp(`datetime`)>=%s and unix_timestamp(`datetime`)<=%s)" % (
        self.schoolid, self.starttime, self.endedtime)
        rs = db.session.execute(sql)
        if len([chrs for chrs in rs]) > 0:
            self.checkscid = 'right'

    def get_enstw_info(self):
        @cache.memoize(timeout=3600 * 12)
        def get_all_user(schoolid, classid, alldescs):
            # 获取学校的所有学生列表
            if classid == '0'or not classid:
                sqlsel = "select DISTINCT userid,username,schoolid,classid,classname from teacher_student_info  " \
                         "where classname!='教师' AND schoolid in (%s)" % (schoolid)
            else:
                sqlsel = "select DISTINCT userid,username,schoolid,classid,classname from teacher_student_info  " \
                     "where classname!='教师' AND classid in (%s)" % (classid)
            data_lists = db.session.execute(sqlsel)
            messes = []
            for datas in data_lists:
                mess = {}
                for x in range(len(datas)):
                    mess[alldescs[x]] = datas[x]
                messes.append(mess)
            return messes

        descnames = ['userId', 'userName', 'schoolId', 'classId', 'className', 'gameCount', 'finCount',
                     'homeFull', 'selfCount', 'selfFull', 'listenFull', 'readFull', 'blankFull', 'listenRate',
                     'readRate', 'blankRate', 'listenNum', 'readNum', 'blankNum']
        if not self.classid or self.classid == '0':
            sqlsel = "SELECT userid,username,schoolid,classid,classname,CAST(SUM(gamecount)AS SIGNED),CAST(SUM(finishcount)AS SIGNED),\
            CAST(SUM(homefull)AS SIGNED),CAST(SUM(selfcount)AS SIGNED),CAST(SUM(selffull)AS SIGNED),CAST(SUM(listenfull)AS SIGNED),\
            CAST(SUM(readfull)AS SIGNED),CAST(SUM(blankfull)AS SIGNED),CAST(AVG(listenrate)AS SIGNED),CAST(AVG(readrate)AS SIGNED),\
            CAST(AVG(blankrate)AS SIGNED),CAST(SUM(listennum)AS SIGNED),CAST(SUM(readnum)AS SIGNED),CAST(SUM(blanknum)AS SIGNED)\
            FROM product_stw_encount WHERE schoolid=%s AND unix_timestamp(`datetime`)>=%s AND unix_timestamp(`datetime`)<=%s GROUP BY userid,username,schoolid,classid,classname" \
                 % (self.schoolid, self.starttime, self.endedtime)
        else:
            sqlsel = "SELECT userid,username,schoolid,classid,classname,CAST(SUM(gamecount)AS SIGNED),CAST(SUM(finishcount)AS SIGNED),\
                          CAST(SUM(homefull)AS SIGNED),CAST(SUM(selfcount)AS SIGNED),CAST(SUM(selffull)AS SIGNED),CAST(SUM(listenfull)AS SIGNED),\
            CAST(SUM(readfull)AS SIGNED),CAST(SUM(blankfull)AS SIGNED),CAST(AVG(listenrate)AS SIGNED),CAST(AVG(readrate)AS SIGNED),\
            CAST(AVG(blankrate)AS SIGNED),CAST(SUM(listennum)AS SIGNED),CAST(SUM(readnum)AS SIGNED),CAST(SUM(blanknum)AS SIGNED)\
             FROM product_stw_encount WHERE classid=%s AND unix_timestamp(`datetime`)>=%s AND unix_timestamp(`datetime`)<=%s GROUP BY userid,username,schoolid,classid,classname" \
                     % (self.classid, self.starttime, self.endedtime)
        data_list = db.session.execute(sqlsel)
        messes = []
        for datas in data_list:
            mess = {}
            for x in range(len(datas)):
                mess[descnames[x]] = datas[x]
            messes.append(mess)
        try:
            student_all = get_all_user(self.schoolid, self.classid, self.alldescs)
        except:
            student_all = []
        alldatas = []
        for allmess in student_all:
            for rdataf in messes:
                if int(rdataf["userId"]) == int(allmess["userId"]):
                    for finone in descnames[5:]:
                        allmess[finone] = rdataf[finone]
                    num_count = allmess['selfCount'] + allmess['gameCount']
                    if allmess['gameCount'] > 0:
                        allmess['finishRate'] = int((allmess['finCount'] / allmess['gameCount'])*1000)/10
                    else:
                        allmess['finishRate'] = 0
                    if num_count > 0:
                        allmess['fullRate'] = int(((allmess['homeFull'] + allmess['selfFull'])/num_count)*1000)/10
                    else:
                        allmess['fullRate'] = 0
                    if allmess['blankNum'] == 0:
                        if allmess['listenNum'] == 0:
                            allmess['rightRate'] = allmess['readRate']
                        else:
                            allmess['rightRate'] = int(((allmess['listenRate'] + allmess['readRate']) / 2)*10)/10
                    else:
                        allmess['rightRate'] = int(((allmess['listenRate']+allmess['readRate']+allmess['blankRate'])/3)*10)/10
            if len(allmess) == len(self.alldescs):
                 for findena in descnames[5:]:
                     allmess[findena] = 0
                 allmess['finishRate'] = allmess['fullRate'] = allmess['rightRate'] = 0
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
        logInfo = str(data['code']) + '[' + data['traceId'] + ']type[getEnStwInfo]' + 'scid[' + str(self.schoolid) \
                  + ']clid[' + str(self.classid) + ']sttime[' + str(self.starttime) + ']endtime[' + str(self.endedtime) + ']'
        log('APIRequest-', logInfo)
        return data

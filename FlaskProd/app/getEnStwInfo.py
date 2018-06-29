from flask import Blueprint, render_template, redirect,request,jsonify
from app import app, cache
from .relog import log
from flask_sqlalchemy import SQLAlchemy
# from .models import Stwdaycount
import time

db = SQLAlchemy(app)
getEnStwInfo = Blueprint('getEnStwInfo', __name__)


def get_trace_id():
    import uuid
    return str(uuid.uuid1()).replace('-', '')


def keep_percent_point_num(num, point):
    # 小数化为百分比，并保留小数位数 num :原数 point:保留位数
    return int(num*10**(point+2))/10**point


@getEnStwInfo.route('/getEnStwInfo', methods=['GET'])
def get_english_stw_info():
    schoolid = request.values.get('schoolId')
    classid = request.values.get('classId', '0')
    starttime = request.values.get('startTime', int(time.time()) - 24*60*60*8)
    endedtime = request.values.get('endTime', int(time.time()))
    if not schoolid:
        trace_id=get_trace_id()
        mess = {'code': 400, 'msg': 'Error! Please enter the correct schoolId!', 'traceId': trace_id}
        log_info = '400' + '[' + trace_id + ']type[getEnStwInfo]' + 'school[No]class[No]' \
                  + 'start[' + str(starttime) + ']end[' + str(endedtime) + ']'
        log('APIRequest-', log_info)
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
        sql = "select distinct school_id from product_stw_encount where school_id in (%s) \
                and (unix_timestamp(`date_time`)>=%s and unix_timestamp(`date_time`)<=%s)" % (
        self.schoolid, self.starttime, self.endedtime)
        rs = db.session.execute(sql)
        if len([chrs for chrs in rs]) > 0:
            self.checkscid = 'right'

    def get_enstw_info(self):
        @cache.memoize(timeout=3600 * 12)
        def get_all_user(schoolid, classid, alldescs):
            # 获取学校的所有学生列表
            if classid == '0'or not classid:
                sql = "select DISTINCT userid,username,schoolid,classid,classname from teacher_student_info  " \
                         "where classname!='教师' AND schoolid in (%s)" % schoolid
            else:
                sql = "select DISTINCT userid,username,schoolid,classid,classname from teacher_student_info  " \
                     "where classname!='教师' AND classid in (%s)" % classid
            data_lists = db.session.execute(sql)
            messes = []
            for datas in data_lists:
                mess = {}
                for x in range(len(datas)):
                    mess[alldescs[x]] = datas[x]
                messes.append(mess)
            return messes

        descnames = ['userId', 'userName', 'schoolId', 'classId', 'className', 'gameCount', 'finCount',
                     'homeFull', 'selfCount', 'selfFull', 'listenFull', 'readFull', 'blankFull', 'fillBlankFull',
                     'listenRate', 'readRate', 'blankRate', 'fillBlankRate', 'listenNum', 'readNum',
                     'blankNum', 'fillBlankNum', 'rightRate']
        if not self.classid or self.classid == '0':
            sql = "SELECT student_id,student_name,school_id,class_id,class_name,CAST(SUM(task_count)AS SIGNED),CAST(SUM(finish_count)AS SIGNED),\
            CAST(SUM(home_full)AS SIGNED),CAST(SUM(self_count)AS SIGNED),CAST(SUM(self_full)AS SIGNED),CAST(SUM(listen_full)AS SIGNED),\
            CAST(SUM(read_full)AS SIGNED),CAST(SUM(blank_full)AS SIGNED),CAST(SUM(fill_blank_full)AS SIGNED), \
            CAST(AVG(IF(listen_num>0,listen_rate,NULL))AS SIGNED),CAST(AVG(IF(read_num>0,read_rate,NULL))AS SIGNED),\
            CAST(AVG(IF(blank_num>0,blank_rate,NULL))AS SIGNED), CAST(AVG(IF(fill_blank_num>0,fill_blank_rate,NULL))AS SIGNED), \
            CAST(SUM(listen_num)AS SIGNED),CAST(SUM(read_num)AS SIGNED),CAST(SUM(blank_num)AS SIGNED),CAST(SUM(fill_blank_num)AS SIGNED),CAST(AVG(rate_avg)AS SIGNED)\
            FROM product_stw_encount WHERE school_id=%s AND unix_timestamp(`date_time`)>=%s AND unix_timestamp(`date_time`)<=%s GROUP BY student_id,student_name,school_id,class_id,class_name" \
                 % (self.schoolid, self.starttime, self.endedtime)
        else:
            sql = "SELECT student_id,student_name,school_id,class_id,class_name,CAST(SUM(task_count)AS SIGNED),CAST(SUM(finish_count)AS SIGNED),\
            CAST(SUM(home_full)AS SIGNED),CAST(SUM(self_count)AS SIGNED),CAST(SUM(self_full)AS SIGNED),CAST(SUM(listen_full)AS SIGNED),\
            CAST(SUM(read_full)AS SIGNED),CAST(SUM(blank_full)AS SIGNED),CAST(SUM(fill_blank_full)AS SIGNED), \
            CAST(AVG(IF(listen_num>0,listen_rate,NULL))AS SIGNED),CAST(AVG(IF(read_num>0,read_rate,NULL))AS SIGNED),\
            CAST(AVG(IF(blank_num>0,blank_rate,NULL))AS SIGNED), CAST(AVG(IF(fill_blank_num>0,fill_blank_rate,NULL))AS SIGNED), \
            CAST(SUM(listen_num)AS SIGNED),CAST(SUM(read_num)AS SIGNED),CAST(SUM(blank_num)AS SIGNED),CAST(SUM(fill_blank_num)AS SIGNED),CAST(AVG(rate_avg)AS SIGNED)\
            FROM product_stw_encount WHERE class_id=%s AND unix_timestamp(`date_time`)>=%s AND unix_timestamp(`date_time`)<=%s GROUP BY student_id,student_name,school_id,class_id,class_name" \
                     % (self.classid, self.starttime, self.endedtime)
        data_list = db.session.execute(sql)
        messes = []
        for datas in data_list:
            mess = {}
            for x in range(len(datas)):
                mess[descnames[x]] = datas[x]
            messes.append(mess)
        try:
            student_all = get_all_user(self.schoolid, self.classid, self.alldescs)
        except Exception as e:
            log(e)
            student_all = tuple()
        alldatas = []
        for allmess in student_all:
            for rdataf in messes:
                if int(rdataf["userId"]) == int(allmess["userId"]):
                    for finone in descnames[5:]:
                        allmess[finone] = rdataf[finone]
                    num_count = allmess['selfCount'] + allmess['gameCount']
                    if allmess['gameCount'] > 0:
                        allmess['finishRate'] = int((allmess['finCount'] / allmess['gameCount'])*10000)/100
                    else:
                        allmess['finishRate'] = 0
                    if num_count > 0:
                        allmess['fullRate'] = int(((allmess['homeFull'] + allmess['selfFull'])/num_count)*10000)/100
                    else:
                        allmess['fullRate'] = 0
                    if allmess['rightRate']:
                        allmess['rightRate'] = int(allmess['rightRate'] * 100)/100
            if len(allmess) == len(self.alldescs):
                 for findena in descnames[5:]:
                     allmess[findena] = 0
                 allmess['finishRate'] = allmess['fullRate'] = 0
            alldatas.append(allmess)
        return alldatas

    def main(self):
        data = dict()
        data['traceId'] = get_trace_id()
        self.check_school_id()
        if self.checkscid == 'right':
            data['code'] = 200
            data['data'] = self.get_enstw_info()
            data['msg'] = 'successful!'
        else:
            data['code'] = 400
            # data['msg'] = 'Error! These schools are not exist!'
            data['msg'] = '该班级在所选时间内暂无数据，请换个班级重试。'
        log_info = str(data['code']) + '[' + data['traceId'] + ']type[getEnStwInfo]' + 'school[' + str(self.schoolid) \
                  + ']class[' + str(self.classid) + ']start[' + str(self.starttime) + ']end[' + str(self.endedtime) + ']'
        log('APIRequest-', log_info)
        return data

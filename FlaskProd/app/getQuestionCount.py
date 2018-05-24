from flask import Blueprint, request, jsonify
from app import app, cache
from .relog import log
import time
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
db = SQLAlchemy(app)

getQstCount = Blueprint('getQstCount', __name__)


def get_trace_id():
    import uuid
    return str(uuid.uuid1()).replace('-', '')


@getQstCount.route('/getQstCount/qstNumAndRate', methods=['POST', 'GET'])  # 指定接口访问的路径，支持什么请求方式get，post
def get_qst_num():
    try:
        school_id = request.values.get('schoolId')  # 获取GET请求的school_id参数传入的值
        start_time = request.values.get('startTime', int(time.time()) - 24*60*60*8)
        end_time = request.values.get('endTime', int(time.time()))
        class_id = request.values.get('classId', 0)
        subject_id = request.values.get('subjectId', 0)
        # user_id = request.values.get('user_id') #支持获取连接拼接的参数，而且还能获取body form填入的参数
        trace_id = get_trace_id()
        if not school_id or class_id == 0 or subject_id == 0:
            mess = {'code': 400, 'msg': 'Please enter the correct school, class and subject!', 'traceId': trace_id}
            log_info = '400' + '[' + trace_id + ']type[getQstNum]' + 'scid[0]clid[0]' + 'start[' + \
                       str(start_time) + ']end[' + str(end_time) + ']'
            log('APIRequest-', log_info)
            return jsonify(mess)
        if not start_time or not end_time:
            mess = {'code': 400, 'msg': 'Please enter the correct time!', 'traceId': trace_id}
            log_info = '400' + '[' + trace_id + ']type[getQstNum]' + 'scid[0]clid[0]' + 'start[' + \
                       str(start_time) + ']end[' + str(end_time) + ']'
            log('APIRequest-', log_info)
            return jsonify(mess)
        else:
            s = GetQuestionNum(school_id=school_id, start_time=start_time, end_time=end_time,
                               subject_id=subject_id, class_id=class_id)
            return jsonify(s.main())
    except AttributeError:
        data = {"code": "405", "msg": "Values error, Check your 'Content-Type' first!"}
        return jsonify(data)


class QuestionNumBase(object):
    def __init__(self, school_id, class_id, start_time, end_time, subject_id):
        self.school_id = str(school_id)
        self.start_time = start_time
        self.end_time = end_time
        self.subject_id = subject_id
        self.class_id = class_id

    def check_school_class_id(self):
        # 检查学校ID 和班级ID
        sql = "SELECT DISTINCT school_id FROM product_qst_count WHERE school_id in (%s) AND class_id in (%s)" \
              % (self.school_id, self.class_id)
        try:
            rs = db.session.execute(sql)
        except:
            rs = tuple()
        if len([i for i in rs]) > 0:
            return True
        return False

    def get_all_user(self):
        # 获取班级的所有学生列表
        @cache.memoize(timeout=3600*24)  # 设置缓存12小时
        def get_all_user_cache(school_id, class_id):
            names = ['userId', 'userName', 'classId', 'className']
            if not class_id or class_id == 0:
                sql = "SELECT DISTINCT userid,username,classid,classname FROM teacher_student_info " \
                         "WHERE classname!='教师' AND schoolid IN (%s)" % school_id
            else:
                sql = "SELECT DISTINCT userid,username,classid,classname FROM teacher_student_info  " \
                         "WHERE classname!='教师' AND classid IN (%s)" % class_id
            data_lists = db.session.execute(sql)
            messes = []
            for data in data_lists:
                mess = {}
                for x in range(len(data)):
                    mess[names[x]] = data[x]
                messes.append(mess)
            return messes
        return get_all_user_cache(self.school_id, self.class_id)


class GetQuestionNum(QuestionNumBase):
    def get_qst_count(self):
        desc_names = ['userId', 'userName', 'classId', 'className', 'subjectId', 'qstNum', 'rightRate']
        sql_select = "SELECT user_id,user_name,class_id,class_name,subject_id,SUM(qst_num),AVG(right_rate)\
              FROM product_qst_count WHERE subject_id = '%s' AND school_id='%s' AND class_id='%s' AND \
              (unix_timestamp(`date_time`)>=%s AND unix_timestamp(`date_time`)<=%s) GROUP BY user_id,user_name,class_id,class_name,subject_id"\
                % (self.subject_id, self.school_id, self.class_id, self.start_time, self.end_time)
        try:
            data_list = db.session.execute(sql_select)
        except:
            data_list = tuple()
        messes = list()
        for data in data_list:
            mess = dict()
            for x in range(len(data)):
                mess[desc_names[x]] = data[x]
            messes.append(mess)
        values = list()
        all_user_data = self.get_all_user()
        if all_user_data:
            for user_data in all_user_data:
                user_data['qstNum'] = 0
                user_data['rightRate'] = '0%'
                user_data['subjectId'] = 0
                for m in messes:
                    if str(m["userId"]) == str(user_data["userId"]):
                        user_data['qstNum'] = int(m['qstNum'])
                        user_data['rightRate'] = str(int(m['rightRate']*10)/10) + '%'
                        user_data['subjectId'] = int(m['subjectId'])
                values.append(user_data)
            return values
        else:
            return messes

    def main(self):
        check_school_class = self.check_school_class_id()
        trace_id = get_trace_id()
        data = dict()
        data['traceId'] = trace_id
        if check_school_class:
            data['code'] = 200
            data['data'] = self.get_qst_count()
            data['msg'] = 'Successful!'
        else:
            data['code'] = 400
            data['msg'] = 'These schools or classes are not exist!'
        log_info = str(data['code']) + '[' + trace_id + ']type[getQstNum]' + 'scid[' + self.school_id + ']' + \
            'start[' + str(self.start_time) + ']' + 'end[' + str(self.end_time) + ']' + 'subid[' + \
            str(self.subject_id) + ']' + 'clid[' + str(self.class_id) + ']'
        log('APIRequest-', log_info)
        return data

from flask import Blueprint, render_template, redirect, request, jsonify
from app import app,cache
from .relog import log
#from .models import Stwdaycount
import json,time,requests
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

getStwInfoRecode = Blueprint('RecodeGetStwInfo',__name__)


def getTraceId():
    import uuid
    return str(uuid.uuid1()).replace('-', '')


@getStwInfoRecode.route('/getstwinfo', methods=['POST', 'GET'])  # 指定接口访问的路径，支持什么请求方式get，post
def get_stwinfo():
    try:
        if request.method == 'POST':
            # userid = request.args.get('userid') # 使用request.args.get方式获取拼接的入参数据
            schoolid = request.json.get('schoolid')  # 获取带json串请求的userid参数传入的值
            starttime = request.json.get('starttime', int(time.time()) - 24*60*60*8)
            endedtime = request.json.get('endedtime', int(time.time()))
            bookid = request.json.get('bookid', '%')
            classid = request.json.get('classid', 0)
            gettype = request.json.get('gettype', 0)
            subjectname = request.json.get('subjectname', 'subname')
        # userid = request.values.get('userid') #支持获取连接拼接的参数，而且还能获取body form填入的参数
        if request.method == 'GET':
            return jsonify({'msg': "Error.You should change the Method to 'Post'!", 'Code': 200, })
        if gettype == 'getbookid':
            s = Getbookid(schoolid)
        elif gettype == 'getstudent':
            s = GetstwStudent(schoolid, starttime, endedtime, subjectname, classid)
        else:
            s = GetStwInfo(school_id=schoolid, start_time=starttime, end_time=endedtime, book_id=bookid, class_id=classid)
        return jsonify(s.main())
            # json.dumps(s.main(), ensure_ascii=False)
    except AttributeError:
        data = {"code": "405", "msg": "Values error, Check your 'Content-Type' first!"}
        return jsonify(data)


@getStwInfoRecode.route('/getLiveHp', methods=['GET'])
def get_stw_livehp():
    password = request.values.get('password')
    school_id = str(request.values.get('schoolId', ''))
    class_id = str(request.values.get('classId', ''))
    if password == 'bigdata123':
        f = StwInfoBase(school_id=school_id, class_id=class_id)
        data = f.get_live_hp()
    else:
        data = {'msg': 'Error, Password was wrong!'}
    return jsonify(data)


@getStwInfoRecode.route('/getLiveIntegral', methods=['GET'])
def get_stw_live_integral():
    password = request.values.get('password')
    school_id = str(request.values.get('schoolId', ''))
    class_id = str(request.values.get('classId', ''))
    book_id = str(request.values.get('bookId', ''))
    start_time = request.values.get('startTime', int(time.time()) - 24 * 60 * 60 * 8)
    end_time = request.values.get('endedTime', int(time.time()))
    if password == 'bigdata123':
        f = StwInfoBase(school_id=school_id, class_id=class_id,
                        book_id=book_id, start_time=start_time, end_time=end_time)
        data = f.get_live_integral()
    else:
        data = {'msg': 'Error, Password was wrong!'}
    return jsonify(data)


@getStwInfoRecode.route('/stwInfoHp/clearCache', methods=['GET'])
def stwcache_clear():
    password = request.values.get('password')
    if password == 'bigdata123':
        cache.clear()
        datas = {'msg': 'Successful! Clear All'}
    else:
        datas = {'msg': 'Error, Password was wrong!'}
    return jsonify(datas)


class StwInfoBase(object):
    # 刷题王数据拉取的父类
    def __init__(self, *args, **kwargs):
        self.school_id = kwargs.get('school_id', '')
        self.class_id = kwargs.get('class_id', 0)
        self.book_id = kwargs.get('book_id', '')
        self.subject_name = kwargs.get('subject_name', '')
        self.start_time = kwargs.get('start_time', int(time.time()) - 24*60*60*8)
        self.end_time = kwargs.get('end_time', int(time.time()))

    def check_school_id(self):
        # 检查学校ID
        sql = "SELECT DISTINCT schoolid FROM product_stw_daycount WHERE schoolid in (%s) \
                        AND (unix_timestamp(`datetime`)>=%s AND unix_timestamp(`datetime`)<=%s)" % (
            self.school_id, self.start_time, self.end_time)
        rs = db.session.execute(sql)
        if len([i for i in rs]) > 0:
            return True
        return False

    def check_book_id(self):
        # 检查书本ID是否存在
        sql = "SELECT DISTINCT schoolid FROM product_stw_daycount WHERE schoolid in (%s) AND bookid IN ('%s') \
                AND (unix_timestamp(`datetime`)>=%s AND unix_timestamp(`datetime`)<=%s)" % (
            self.school_id, self.book_id, self.start_time, self.end_time)
        rs = db.session.execute(sql)
        if len([i for i in rs]) > 0:
            return True
        return False

    def get_all_user(self):
        # 获取班级的所有学生列表
        @cache.memoize(timeout=3600*12)  # 设置缓存12小时
        def get_all_user_cache(school_id, class_id):
            names = ['userid', 'username', 'schoolid', 'classname']
            if not class_id or class_id == 0:
                sqlsel = "SELECT DISTINCT userid,username,schoolid,classname FROM teacher_student_info " \
                         "WHERE classname!='教师' AND schoolid IN (%s)" % school_id
            else:
                sqlsel = "SELECT DISTINCT userid,username,schoolid,classname FROM teacher_student_info  " \
                         "WHERE classname!='教师' AND schoolid IN (%s) and classid IN (%s)" % (school_id, class_id)
            data_lists = db.session.execute(sqlsel)
            messes = []
            for datas in data_lists:
                mess = {}
                for x in range(len(datas)):
                    mess[names[x]] = datas[x]
                messes.append(mess)
            return messes
        return get_all_user_cache(self.school_id, self.class_id)

    def get_live_hp(self):
        # 调取业务实时数据接口，取得数据
        @cache.memoize(timeout=3000)
        def get_live_student_hp(school_id, class_id):
            # 获取学生的实时的体力和诚信分，访问 Mongo 库
            import pymongo
            mongo_url = "172.16.10.28:50000"
            client = pymongo.MongoClient(mongo_url)
            mongo_db = client.xh_king
            projection_fields = {'_id': False, 'studentId': True, 'hp': True, 'credit': True,
                                 'schoolId': True, 'classId': True, 'grade': True}
            if not class_id:
                query_args = {"schoolId": {"$in": list(map(int, str(school_id).split(',')))}}
            else:
                query_args = {"classId": {"$in": list(map(int, str(class_id).split(',')))}}
            results = mongo_db.student.find(query_args, projection=projection_fields)
            data = list()
            if results:
                for result in results:
                    data.append(result)
            return data

        @cache.memoize(timeout=3000)
        def get_hp(school_ids, class_ids):  # java提供接口 ## 20180409已停用
            url = 'http://127.0.0.1:18889/student/studentInfo'
            # url = 'http://bigdata.yunzuoye.net/student/studentInfo'
            if class_ids is None or class_ids == 0:
                data = {"schoolIds": school_ids, "password": "king123456", }
            else:
                data = {"schoolIds": school_ids, "password": "king123456", "classIds": class_ids}
            try:
                req_data = requests.get(url, params=data, timeout=2).json()
            except TimeoutError or ValueError:
                req_data = []
            return req_data

        return get_live_student_hp(self.school_id, self.class_id)

    def get_live_integral(self):
        @cache.memoize(timeout=3600)
        def get_live_student_integral(school_id='', class_id='', book_id='', start_time=0, end_time=0):
            # 获取学生每局的得分求和，返回学生ID和对应的分数
            import pymongo
            mongo_url = "172.16.10.28:50000"
            client = pymongo.MongoClient(mongo_url)
            mongo_db = client.xh_king
            projection_fields = {'_id': False, 'studentId': True, 'integral': True,
                                 'schoolId': True, 'classId': True}
            if not class_id:  # 表结构中没有schoolId 这个字段，如过没有传入classId 则需要从其他表中根据学校取班级
                query_args_school = {"schoolId": {"$in": list(map(int, str(school_id).split(',')))}}
                projection_fields_school = {'_id': False, 'studentId': True, 'schoolId': True, 'classId': True}
                results_school = mongo_db.student.find(query_args_school, projection=projection_fields_school)
                class_ids = list()
                if results_school:
                    for result_school in results_school:
                        class_ids.append(result_school['classId'])
                    class_ids = list(set(class_ids))  # 返回一个班级ID 列表的集合
                query_args = {'bookId': book_id, 'classId': {"$in": class_ids},
                              'createTime': {"$gte": start_time * 1000, "$lte": end_time * 1000}}
            else:
                query_args = {'bookId': book_id, 'classId': {"$in": list(map(int, str(class_id).split(',')))},
                              'createTime': {"$gte": start_time * 1000, "$lte": end_time * 1000}}
            results = mongo_db.game.find(query_args, projection=projection_fields)
            user_datas = list()
            if results:
                data = list()
                user_sets = list()
                for result in results:
                    user_sets.append(result['studentId'])
                    data.append(result)
                user_sets = list(set(user_sets))
                for user_id in user_sets:
                    fin_data = dict()
                    fin_data['integral'] = 0
                    for user_data in data:
                        if user_data['studentId'] == user_id:
                            fin_data['integral'] += user_data['integral']
                    fin_data['integral'] = fin_data['integral']
                    fin_data['studentId'] = user_id
                    user_datas.append(fin_data)
            return user_datas
        return get_live_student_integral(self.school_id, self.class_id, self.book_id, self.start_time ,self.end_time)

    def get_sub_type(self):
        sqlsel = "SELECT DISTINCT subtype FROM product_stw_subject WHERE bookid IN ('%s')" % self.book_id
        data_list = db.session.execute(sqlsel)
        for x in data_list:
            data = x[0]
            return data
        else:
            return 1


class Getbookid(object):

    def findallbookid(self):
        # 获取所有书本ID对应书名
        sqlsel = "select distinct bookname,bookid,subtype from product_stw_subject"
        descnames = ['bookname', 'bookid','subtype']
        data_list = db.session.execute(sqlsel)
        messes = []
        for datas in data_list:
            mess = {}
            for x in range(len(datas)):
                mess[descnames[x]] = datas[x]
            messes.append(mess)
        return messes

    def main(self):
        datav = Getbookid.findallbookid(self)
        traceId = getTraceId()
        data = {}
        data['traceId'] = traceId
        data['code'] = 200
        data['data'] = datav
        data['msg'] = 'Successful!'
        logInfo = str(data['code'])+'['+ traceId + ']type[getBookid]' + 'scid[All]'
        log('APIRequest-', logInfo)
        # log('logInfo:Getbookid - ', data['code'])
        return data


class GetStwInfo(StwInfoBase):
    # 获取数据的主类
    def get_king_info(self):
        # 数据拉取的主函数
        desc_names = ['userid', 'username', 'schoolid', 'schoolname', 'classname', 'bookid', 'bookname',
                'countscore', 'numhomework', 'numselfwork','topicnum', 'countright', 'rightlv', 'counttime', 'topicold']
        subtype_result = self.get_sub_type()
        if subtype_result == 1:
            if not self.class_id or self.class_id == 0:
                sql = "SELECT userid,username,schoolid,schoolname,classname,bookid,bookname,countscore,CAST(SUM(numhomework)AS SIGNED),\
                        CAST(SUM(numselfwork)AS SIGNED),CAST(SUM(topicnum)AS SIGNED),CAST(SUM(countright)AS SIGNED),CAST(SUM(countright)*100/SUM(topicnum)AS SIGNED),\
                        CAST(SUM(counttime)/(SUM(numhomework)+SUM(numselfwork))AS SIGNED),CAST((SUM(numhomework)+SUM(numselfwork))*10 AS SIGNED) \
                        FROM product_stw_daycount WHERE schoolid IN (%s)AND (unix_timestamp(`datetime`) >= %s AND unix_timestamp(`datetime`) <= %s)\
                        AND bookid LIKE '%s' GROUP BY userid,username,schoolid,schoolname,classname,bookname,countscore,bookid" \
                         % (self.school_id, self.start_time, self.end_time, self.book_id)
            else:
                sql = "SELECT userid,username,schoolid,schoolname,classname,bookid,bookname,countscore,CAST(SUM(numhomework)AS SIGNED),\
                        CAST(SUM(numselfwork)AS SIGNED),CAST(SUM(topicnum)AS SIGNED),CAST(SUM(countright)AS SIGNED),CAST(SUM(countright)*100/SUM(topicnum)AS SIGNED),\
                        CAST(SUM(counttime)/(SUM(numhomework)+SUM(numselfwork))AS SIGNED),CAST((SUM(numhomework)+SUM(numselfwork))*10 AS SIGNED) \
                        FROM product_stw_daycount WHERE classid IN (%s)AND (unix_timestamp(`datetime`) >= %s AND unix_timestamp(`datetime`) <= %s)\
                        AND bookid LIKE '%s' GROUP BY userid,username,schoolid,schoolname,classname,bookname,countscore,bookid" \
                         % (self.class_id, self.start_time, self.end_time, self.book_id)
        elif subtype_result == 2:
            if not self.class_id or self.class_id == 0:
                sql = "SELECT userid,username,schoolid,schoolname,classname,bookid,bookname,countscore,CAST(SUM(numhomework)AS SIGNED),\
                        CAST(SUM(numselfwork)AS SIGNED),CAST(SUM(topicnum)/10 AS SIGNED),CAST(SUM(countright)AS SIGNED),CAST(SUM(rightlv)/SUM(topicnum)AS SIGNED),\
                        CAST(SUM(counttime)*10/(SUM(topicnum))AS SIGNED),CAST(SUM(numhomework)+SUM(numselfwork)AS SIGNED) \
                        FROM product_stw_daycount WHERE schoolid IN (%s)AND (unix_timestamp(`datetime`) >= %s AND unix_timestamp(`datetime`) <= %s)\
                        AND bookid LIKE '%s' GROUP BY userid,username,schoolid,schoolname,classname,bookname,countscore,bookid" \
                         % (self.school_id, self.start_time, self.end_time, self.book_id)
            else:
                sql = "SELECT userid,username,schoolid,schoolname,classname,bookid,bookname,countscore,CAST(SUM(numhomework)AS SIGNED),\
                        CAST(SUM(numselfwork)AS SIGNED),CAST(SUM(topicnum)/10 AS SIGNED),CAST(SUM(countright)AS SIGNED),CAST(SUM(rightlv)/SUM(topicnum)AS SIGNED),\
                        CAST(SUM(counttime)*10/(SUM(topicnum))AS SIGNED),CAST(SUM(numhomework)+SUM(numselfwork)AS SIGNED)\
                        FROM product_stw_daycount WHERE classid IN (%s)AND (unix_timestamp(`datetime`) >= %s AND unix_timestamp(`datetime`) <= %s)\
                        AND bookid LIKE '%s' GROUP BY userid,username,schoolid,schoolname,classname,bookname,countscore,bookid" \
                         % (self.class_id, self.start_time, self.end_time, self.book_id)
        data_list = db.session.execute(sql)
        messes = []
        for data in data_list:
            mess = {}
            for x in range(len(data)):
                mess[desc_names[x]] = data[x]
            messes.append(mess)
        try:
            live_hp_data = self.get_live_hp()
        except:
            live_hp_data = []
        try:
            live_integral_data = self.get_live_integral()
        except:
            live_integral_data = []
        all_user_data = self.get_all_user()
        values = []
        for user_data in all_user_data:
            user_data["hp"] = 0
            user_data["credit"] = 0
            user_data["integral"] = 0
            for m in messes:
                book_name = m['bookname']
                if str(m["userid"]) == str(user_data["userid"]):
                    user_data["countscore"] = m["countscore"]
                    user_data["numhomework"] = m["numhomework"]
                    user_data["numselfwork"] = m["numselfwork"]
                    user_data["topicnum"] = m["topicnum"]
                    user_data["countright"] = m["countright"]
                    user_data["rightlv"] = m["rightlv"]
                    user_data["counttime"] = m["counttime"]
                    user_data["topicold"] = m["topicold"]
                else:
                    for desc_name in desc_names[7:]:
                        user_data[desc_name] = 0
            for hp_data in live_hp_data:
                if str(hp_data['studentId']) == str(user_data["userid"]):
                    user_data["hp"] = hp_data["hp"]
                    user_data["credit"] = hp_data["credit"]
                else:
                    user_data["hp"] = user_data["credit"] = 0
            for integral_data in live_integral_data:
                if str(user_data['userid']) == str(integral_data['studentId']):
                    user_data["integral"] = integral_data["integral"]
                else:
                    user_data["integral"] = 0
            user_data['bookname'] = book_name
            values.append(user_data)
        return values

    def main(self):
        #  判定有学校ID和对应的书本ID后，再执行数据拉取，并写入日志
        check_school_result = self.check_school_id()
        check_book_result = self.check_book_id()
        traceId = getTraceId()
        data = dict()
        data['traceId'] = traceId
        if check_school_result is True and check_book_result is True:
            data['code'] = 200
            data['data'] = GetStwInfo.get_king_info(self)
            data['msg'] = 'Successful!'
        else:
            data['code'] = 400
            data['msg'] = 'These schools or books are not exist!'
        logInfo = str(data['code']) + '[' + traceId + ']type[getStwinfo]' + 'scid[' + self.school_id + ']'\
                  + 'sttime[' + str(self.start_time) + ']' + 'endtime[' + str(self.end_time) + ']' + 'bkid[' +\
                str(self.book_id) + ']' + 'clid[' + str(self.class_id) + ']'
        log('APIRequest-', logInfo)
        return data


class GetstwStudent(StwInfoBase):

    def getstwstudent(self):
        subpart = {'语文': 1, '数学': 2, '英语': 3, '科学': 4, '历史': 5, '道德与法治': 6, '物理': 7}
        subject_id = subpart.get(self.subject_name)
        self.alldescs = ['userid', 'username']
        descnames=['userid', 'username', 'oldtopicnum', 'topicnum', 'rightnum']
        sql="SELECT userid,username,SUM(oldtopicnum)AS `oldtopicnum`,SUM(topicnum)AS `topicnum`,sum(countright)AS rightnum FROM product_stw_subcount " \
            "WHERE classid = %s AND subjectid = %s AND unix_timestamp(`datetime`)>=%s and unix_timestamp(`datetime`)<=%s GROUP BY userid,username"\
            % (self.classid, subject_id, self.starttime, self.endedtime)
        data_list = db.session.execute(sql)
        messes = []
        for datas in data_list:
            mess = {}
            for x in range(len(datas)):
                mess[descnames[x]] = datas[x]
            mess['rightrate']=int((mess['rightnum']/mess['topicnum'])*10000)/100
            messes.append(mess)
        allmesses = self.get_all_user()
        findescnames = ['userid', 'username', 'topicnum', 'rightnum', 'rightrate']
        alldatas = []
        for allmess in allmesses:
            for rdataf in messes:
                if str(rdataf["userid"]) == str(allmess["userid"]):
                    allmess["username"] = rdataf["username"]
                    allmess["topicnum"] = rdataf["oldtopicnum"]*10
                    allmess["rightnum"] = rdataf["rightnum"]
                    allmess["rightrate"] = rdataf["rightrate"]
            if len(allmess) == len(self.alldescs):
                allmess["topicnum"]=allmess["rightnum"]=allmess["rightrate"]=0
                # for findena in findescnames:
                #     allmess[findena] = 0
            alldatas.append(allmess)
        return alldatas

    def main(self):
        self.checkclassid()
        traceId = getTraceId()
        if self.classid and self.schoolid and self.subjectid:
            if self.checkclid == 'right':
                datav = self.getstwstudent()
                codenum = 200
                messa='successful!'
            else:
                datav = 'No data!'
                codenum = 400
                messa = 'Error, Classid not exists!'
            logInfo = str(codenum) + '[' + traceId + ']type[getStudent]' + 'scid['+ str(self.schoolid)+ ']classid['+ str(self.classid) +\
                      ']subjectid['+ str(self.subjectid) + ']sttime[' + str(self.starttime) + ']' + 'endtime[' + str(self.endedtime) + ']'
        elif not self.classid or not self.schoolid:
            datav = 'No data!'
            codenum = 400
            messa = 'Classid or schoolid not exists!'
            logInfo = str(codenum) + '[' + traceId + ']type[getStudent]subname[' + str(self.subjectname) + \
                      ']sttime['+ str(self.starttime) +']'+ 'endtime['+ str(self.endedtime) + ']'
        elif not self.subjectid:
            datav = 'No data!'
            codenum = 400
            messa = 'SubjectName not exists!'
            logInfo = str(codenum) + '[' +traceId + ']type[getStudent]subname[' + str(self.subjectname) + \
                      ']sttime[' + str(self.starttime) + ']' + 'endtime[' + str(self.endedtime) + ']'
        data = {}
        data['traceId'] = traceId
        data['code'] = codenum
        data['data'] = datav
        data['msg'] = messa
        log('APIRequest-', logInfo)
        # log('logInfo:Getbookid - ', data['code'])
        return data


@getStwInfoRecode.route('/getid', methods=['GET'])
@cache.cached(timeout=10, key_prefix='view_%s', unless=None)
def getid():
    print("cachetest")
    return jsonify({'test success': 1131231})


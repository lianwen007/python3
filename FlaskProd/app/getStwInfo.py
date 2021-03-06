from flask import Blueprint, render_template, redirect,request,jsonify
from app import app,cache
from .relog import log
#from .models import Stwdaycount
import json,time,requests
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

getStwInfo = Blueprint('getStwInfo',__name__)


def getTraceId():
    import uuid
    return str(uuid.uuid1()).replace('-', '')


@getStwInfo.route('/getstwinfo', methods=['POST', 'GET'])  # 指定接口访问的路径，支持什么请求方式get，post
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
            subjectname = request.json.get('subjectname','subname')
        # userid = request.values.get('userid') #支持获取连接拼接的参数，而且还能获取body form填入的参数
        if request.method == 'GET':
            return jsonify({'msg': "Error.You should change the Method to 'Post'!", 'Code': 405, })
        if gettype == 'getbookid':
            s = Getbookid(schoolid)
        elif gettype == 'getstudent':
            s = GetstwStudent(schoolid, starttime, endedtime, subjectname, classid)
        else:
            s = Getstwinfo(schoolid, starttime, endedtime, bookid, classid)
        return jsonify(s.main())
            # json.dumps(s.main(), ensure_ascii=False)
    except AttributeError:
        data = {"code": "405", "msg": "Values error, Check your 'Content-Type' first!"}
        return jsonify(data)


@getStwInfo.route('/getLiveHp', methods=['GET'])
def get_stw_livehp():
    password = request.values.get('password')
    school_id = str(request.values.get('schoolId', ''))
    class_id = str(request.values.get('classId', ''))
    if password == 'bigdata123':
        data = get_live_student_hp(school_id, class_id)
    else:
        data = {'msg': 'Error, Password was wrong!'}
    return jsonify(data)


@getStwInfo.route('/getLiveIntegral', methods=['GET'])
def get_stw_live_integral():
    password = request.values.get('password')
    school_id = str(request.values.get('schoolId', ''))
    class_id = str(request.values.get('classId', ''))
    book_id = str(request.values.get('bookId', ''))
    starttime = request.values.get('startTime', int(time.time()) - 24 * 60 * 60 * 8)
    endedtime = request.values.get('endedTime', int(time.time()))
    if password == 'bigdata123':
        data = get_live_student_integral(school_id, class_id, book_id, starttime, endedtime)
    else:
        data = {'msg': 'Error, Password was wrong!'}
    return jsonify(data)


@getStwInfo.route('/stwInfoHp/clearCache', methods=['GET'])
def stwcache_clear():
    password = request.values.get('password')
    if password == 'bigdata123':
        cache.clear()
        datas = {'msg': 'Successful! Clear All'}
    else:
        datas = {'msg': 'Error, Password was wrong!'}
    return jsonify(datas)


class Getstwinfo(object):
    def __init__(self, schoolid, starttime, endedtime, bookid, classid):
        self.schoolid = str(schoolid)
        self.starttime = starttime
        self.endedtime = endedtime
        self.bookid = bookid
        self.classid = classid
        self.checkscid = ''
        self.checkBookid=''
        self.alldescs = ['userid', 'username', 'schoolid', 'classname']

    def checkschoolid(self):
        # 检查学校ID是否存在
        sql = "select distinct schoolid from product_stw_daycount where schoolid in (%s) \
                and (unix_timestamp(`datetime`)>=%s and unix_timestamp(`datetime`)<=%s)" % (
        self.schoolid, self.starttime, self.endedtime)
        rs = db.session.execute(sql)
        if len([chrs for chrs in rs ])>0:
            self.checkscid = 'right'

    def checkbookid(self):
        # 检查书本ID是否存在
        sql = "select distinct schoolid from product_stw_daycount where schoolid in (%s) and bookid in ('%s') \
                and (unix_timestamp(`datetime`)>=%s and unix_timestamp(`datetime`)<=%s)" % (
            self.schoolid,self.bookid, self.starttime, self.endedtime)
        rs = db.session.execute(sql)
        if len([chrs for chrs in rs ])>0:
            self.checkBookid = 'right'

    def get_all_user(self):
        # 获取学校或班级的所有学生列表
        alldescs=self.alldescs
        if self.classid is None or self.classid == '' or self.classid == 0:
            sqlsel = "select DISTINCT userid,username,schoolid,classname from teacher_student_info " \
                     "where classname!='教师' AND schoolid in (%s)" % (self.schoolid)
        else:
            sqlsel = "select DISTINCT userid,username,schoolid,classname from teacher_student_info  " \
                     "where classname!='教师' AND schoolid in (%s) and classid in (%s)"% (self.schoolid,self.classid)
        data_lists = db.session.execute(sqlsel)
        messes = []
        for datas in data_lists:
            mess = {}
            for x in range(len(datas)):
                mess[alldescs[x]] = datas[x]
            messes.append(mess)
        return messes

    def get_subType(self):
        self.checkBookid
        if self.checkBookid == 'right':
            sqlsel = "select DISTINCT subtype from product_stw_subject WHERE bookid in ('%s')" % (self.bookid)
            data_list = db.session.execute(sqlsel)
            for x in data_list:
                datas = x[0]
                return datas
        else:
            return 0

    def get_book_name(self):
        if self.bookid:
            sqlsel = "select DISTINCT bookname from product_stw_subject WHERE bookid in ('%s')" % (self.bookid)
            data_list = db.session.execute(sqlsel)
            for x in data_list:
                datas = x[0]
                return datas

    def getkinginfo(self):
        # 数据拉取的主函数
        @cache.memoize(timeout=3000)
        def get_live_hp(schoolIds, classIds):
            # 调取业务实时数据接口，取得数据 ### 20180409已停用
            url = 'http://127.0.0.1:18889/student/studentInfo'
            # url = 'http://bigdata.yunzuoye.net/student/studentInfo'
            if classIds is None or classIds == '' or classIds == 0:
                getdata = {"schoolIds": schoolIds, "password": "king123456", }
            else:
                getdata = {"schoolIds": schoolIds, "password": "king123456", "classIds": classIds}
            try:
                reqdatas = requests.get(url, params=getdata, timeout=2).json()
            except:
                reqdatas = []
                #cache.delete_memoized('get_live_hp', schoolIds, classIds)
            return reqdatas

        descnames = ['userid', 'username', 'schoolid', 'schoolname', 'classname', 'classid',
                     'bookname', 'bookid', 'hp', 'credit', 'countscore', 'numhomework', 'numselfwork',
                     'topicnum', 'countright', 'rightlv', 'counttime', 'datetime']
        if not self.classid or self.classid == ''or self.classid == 0:
            sqlsel = "select * from product_stw_daycount where schoolid in (%s) \
                and (unix_timestamp(`datetime`)>=%s and unix_timestamp(`datetime`)<=%s) \
                and bookid like '%s' order by `datetime` DESC " % (self.schoolid, self.starttime, self.endedtime, self.bookid)
        else:
            sqlsel = "select * from product_stw_daycount where schoolid in (%s) \
                and (unix_timestamp(`datetime`)>=%s and unix_timestamp(`datetime`)<=%s) \
                and classid in (%s) and bookid like '%s' order by `datetime` DESC " % (self.schoolid, self.starttime, self.endedtime, self.classid, self.bookid)
        data_list = db.session.execute(sqlsel)
        messes, mesind, finad = [], [], []
        for datas in data_list:
            mess = {}
            for x in range(len(datas)):
                mess[descnames[x]] = datas[x]
            messes.append(mess)
        for mes in messes:
            mesind.append(mes['userid'])
        mesindex = list(set(mesind))
        for y in mesindex:
            # findata=[]
            dataz = []
            for mes in messes:
                if mes['userid'] == y:
                    dataz.append(mes)
            # findata.append(dataz)
            finad.append(dataz)
        rdatafin = []
        if self.get_subType() == 1:
            for dataf in finad:
                rdata = {}
                num = [0, 0, 0, 0, 0, 0]
                for z in range(len(dataf)):
                    for i in range(len(dataf[z])):
                        if i <= 10:
                            rdata[descnames[i]] = dataf[0][descnames[i]]
                        elif i <= 16:
                            if not dataf[z][descnames[i]]:
                                dataf[z][descnames[i]] = 0
                            num[i - 11] += dataf[z][descnames[i]]
                            rdata[descnames[i]] = num[i - 11]
                        else:
                            if rdata[descnames[13]] == 0:
                                rdata[descnames[15]] = rdata[descnames[16]] = 0
                            else:
                                rdata[descnames[15]] = int((rdata[descnames[14]] / rdata[descnames[13]]) * 1000) / 10
                                rdata[descnames[16]] = int((rdata[descnames[16]] / rdata[descnames[13]]) * 10) / 10
                # rdata['topicOld'] = (rdata[descnames[11]] + rdata[descnames[12]])*10
                rdatafin.append(rdata)
        elif self.get_subType() == 2:
            for dataf in finad:
                rdata = {}
                num = [0, 0, 0, 0, 0, 0]
                for z in range(len(dataf)):
                    for i in range(len(dataf[z])):
                        if i <= 10:
                            rdata[descnames[i]] = dataf[0][descnames[i]]
                        elif i <= 16:
                            if not dataf[z][descnames[i]]:
                                dataf[z][descnames[i]] = 0
                            num[i - 11] += dataf[z][descnames[i]]
                            rdata[descnames[i]] = num[i - 11]
                        else:
                            if rdata[descnames[13]] == 0:
                                rdata[descnames[15]] = rdata[descnames[16]] = 0
                            else:
                                rdata[descnames[13]] = rdata[descnames[13]]/10
                               # rdata[descnames[15]] = int((rdata[descnames[15]] / len(dataf)) * 100) / 100
                                rdata[descnames[15]] = int((rdata[descnames[15]] / rdata[descnames[13]]) * 100) / 100
                                rdata[descnames[16]] = int((rdata[descnames[16]] / rdata[descnames[13]]) * 10) / 10
                rdatafin.append(rdata)
        try:
            reqdatas = get_live_student_hp(self.schoolid, self.classid)
        except:
            reqdatas = []
        allmesses = self.get_all_user()
        findescnames = ['countscore', 'numhomework', 'numselfwork', 'topicnum', 'countright', 'rightlv', 'counttime']
        alldatas = []
        for allmess in allmesses:
            for rdataf in rdatafin:
                if str(rdataf["userid"]) == str(allmess["userid"]):
                    allmess["countscore"] = rdataf["countscore"]
                    allmess["numhomework"] = rdataf["numhomework"]
                    allmess["numselfwork"] = rdataf["numselfwork"]
                    allmess["topicnum"] = rdataf["topicnum"]
                    allmess["countright"] = rdataf["countright"]
                    allmess["rightlv"] = rdataf["rightlv"]
                    allmess["counttime"] = rdataf["counttime"]
            if len(allmess) == len(self.alldescs):
                for findena in findescnames:
                    allmess[findena] = 0
            allmess['topicold'] = (allmess[descnames[11]] + allmess[descnames[12]])*10
            alldatas.append(allmess)
        lastdatas = []
        for adatas in alldatas:
            for reqdata in reqdatas:
                if str(reqdata["studentId"]) == str(adatas["userid"]):
                    adatas["hp"] = reqdata["hp"]
                    adatas["credit"] = reqdata["credit"]
            if len(adatas) == len(self.alldescs) + len(findescnames) + 1:
                adatas["credit"] = adatas["hp"] = 0
            adatas['bookname'] = self.get_book_name()
            adatas['integral'] = 0
            lastdatas.append(adatas)
        try:
            students_integral = get_live_student_integral(self.schoolid, self.classid, self.bookid, self.starttime, self.endedtime)
        except:
            students_integral = []
        fin_datas = list()
        for lastdata in lastdatas:
            if students_integral:
                for student_integral in students_integral:
                    if str(lastdata['userid']) == str(student_integral['studentId']):
                        lastdata['integral'] = student_integral['integral']
            fin_datas.append(lastdata)
        return fin_datas

    def main(self):
        #  判定有学校ID和对应的书本id后，再执行数据拉取，并写入日志
        self.checkschoolid()
        self.checkbookid()
        traceId = getTraceId()
        data = {}
        data['traceId']= traceId
        if self.checkscid == 'right' and self.checkBookid == 'right':
            data['code'] = 200
            data['data'] = Getstwinfo.getkinginfo(self)
            data['msg'] = 'Successful!'
        else:
            data['code'] = 400
            data['msg'] = 'These schools or books are not exist!'
        logInfo = str(data['code']) + '[' + traceId + ']type[getStwinfo]' + 'scid[' + self.schoolid + ']'\
                  + 'sttime[' + str(self.starttime) + ']' + 'endtime[' + str(self.endedtime) + ']' + 'bkid[' +\
                str(self.bookid) + ']' + 'clid[' + str(self.classid) + ']'
        log('APIRequest-', logInfo)
        return data


class Getbookid(object):
    def __init__(self, schoolid):
        self.schoolid = schoolid

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
    def findbookidbysc(self):
        # 根据学校ID获取书本ID和对应书名，已暂停使用
        sqlsel = "select distinct bookname,bookid from product_stw_daycount where schoolid in (%s)" % (
            self.schoolid)
        descnames = ['bookname', 'bookid']
        data_list  = db.session.execute(sqlsel)
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


class GetstwStudent(object):
    def __init__(self,schoolid, starttime, endedtime, subjectname , classid):
        subpart={"语文":1,"数学":2,"英语":3,"科学":4,"历史":5,"道德与法治":6,"物理":7,}
        self.subjectname=subjectname
        self.schoolid = str(schoolid)
        self.starttime = starttime
        self.endedtime = endedtime
        self.subjectid = subpart.get(self.subjectname)
        self.classid = classid
        self.checkclid=''
        self.alldescs=['userid','username']

    def checkclassid(self):
        # 检查学校ID是否存在
        sql = "select distinct classid from product_stw_daycount where classid in (%s) \
                and (unix_timestamp(`datetime`)>=%s and unix_timestamp(`datetime`)<=%s)" % (
        self.classid, self.starttime, self.endedtime)
        rs = db.session.execute(sql)
        if len([chrs for chrs in rs ])>0:
            self.checkclid = 'right'

    def getstwstudent(self):
        @cache.memoize(timeout=3600*12)
        def get_all_user(classid,alldescs):
            # 获取班级的所有学生列表
            sqlsel = "select DISTINCT userid,username from teacher_student_info  " \
                     "where classname!='教师' AND classid in (%s)" % (classid)
            data_lists = db.session.execute(sqlsel)
            messes = []
            for datas in data_lists:
                mess = {}
                for x in range(len(datas)):
                    mess[alldescs[x]] = datas[x]
                messes.append(mess)
            return messes

        descnames=['userid', 'username', 'oldtopicnum', 'topicnum', 'rightnum']
        sql="SELECT userid,username,SUM(oldtopicnum)AS `oldtopicnum`,SUM(topicnum)AS `topicnum`,sum(countright)AS rightnum FROM product_stw_subcount " \
            "WHERE classid = %s AND subjectid = %s AND unix_timestamp(`datetime`)>=%s and unix_timestamp(`datetime`)<=%s GROUP BY userid,username"\
            %(self.classid, self.subjectid, self.starttime, self.endedtime)
        data_list = db.session.execute(sql)
        messes = []
        for datas in data_list:
            mess = {}
            for x in range(len(datas)):
                mess[descnames[x]] = datas[x]
            mess['rightrate']=int((mess['rightnum']/mess['topicnum'])*10000)/100
            messes.append(mess)
        allmesses = get_all_user(self.classid,self.alldescs)
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
                datav=self.getstwstudent()
                codenum=200
                messa='successful!'
            else:
                datav = 'No data!'
                codenum = 400
                messa = 'Error, Classid not exists!'
            logInfo = str(codenum) + '[' + traceId + ']type[getStudent]'  + 'scid['+ str(self.schoolid)+ ']classid['+ str(self.classid) +\
                      ']subjectid['+ str(self.subjectid) + ']sttime[' + str(self.starttime) + ']' + 'endtime[' + str(self.endedtime) + ']'
        elif not self.classid or not self.schoolid:
            datav = 'No data!'
            codenum = 400
            messa = 'Classid or schoolid not exists!'
            logInfo = str(codenum) +'['+ traceId + ']type[getStudent]subname['+ str(self.subjectname) + ']sttime['+ str(self.starttime) +']'+ 'endtime['+ str(self.endedtime) + ']'
        elif not self.subjectid:
            datav = 'No data!'
            codenum = 400
            messa = 'SubjectName not exists!'
            logInfo = str(codenum) +'['+traceId + ']type[getStudent]subname['+ str(self.subjectname) + ']sttime['+ str(self.starttime) +']'+ 'endtime['+ str(self.endedtime) + ']'
        data = {}
        data['traceId'] = traceId
        data['code'] = codenum
        data['data'] = datav
        data['msg'] = messa
        log('APIRequest-', logInfo)
        # log('logInfo:Getbookid - ', data['code'])
        return data


@cache.memoize(timeout=3000)
def get_live_student_hp(schoolid='', classid=''):
    # 获取学生的实时的体力和诚信分
    import pymongo
    mongo_url = "172.16.10.28:50000"
    client = pymongo.MongoClient(mongo_url)
    mongo_db = client.xh_king
    projection_fields = {'_id': False, 'studentId': True, 'hp': True, 'credit': True,
                         'schoolId': True, 'classId': True, 'grade': True}
    if not classid:
        query_args = {"schoolId": {"$in": list(map(int, str(schoolid).split(',')))}}
    else:
        query_args = {"classId": {"$in": list(map(int, str(classid).split(',')))}}
    results = mongo_db.student.find(query_args, projection=projection_fields)
    data = list()
    if results:
        for result in results:
            data.append(result)
    return data


@cache.memoize(timeout=3600)
def get_live_student_integral(schoolid='', classid='', book_id='', start_time=0, end_time=0):
    # 获取学生每局的得分求和，返回学生ID和对应的分数
    import pymongo
    mongo_url = "172.16.10.28:50000"
    client = pymongo.MongoClient(mongo_url)
    mongo_db = client.xh_king
    projection_fields = {'_id': False, 'studentId': True, 'integral': True,
                         'schoolId': True, 'classId': True}
    if not classid:
        query_args_school = {"schoolId": {"$in": list(map(int, str(schoolid).split(',')))}}
        projection_fields_school = {'_id': False, 'studentId': True,
                                    'schoolId': True, 'classId': True}
        results_school = mongo_db.student.find(query_args_school, projection=projection_fields_school)
        class_ids = list()
        if results_school:
            for result_school in results_school:
                class_ids.append(result_school['classId'])
            class_ids = list(set(class_ids))
        query_args = {
            "bookId": book_id,
            "classId": {"$in": class_ids},
            "createTime": {"$gte": start_time * 1000, "$lte": end_time * 1000}
        }
    else:
        query_args = {
            "bookId": book_id,
            "classId": {"$in": list(map(int, str(classid).split(',')))},
            "createTime": {"$gte": start_time * 1000, "$lte": end_time * 1000}
        }
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


@getStwInfo.route('/getid', methods=['GET'])
@cache.cached(timeout=10, key_prefix='view_%s', unless=None)
def getid():
    print("cachetest")
    return jsonify({'test success': 1131231})


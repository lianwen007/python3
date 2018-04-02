from flask import Blueprint, render_template, redirect,request,jsonify
from app import app,cache
from .relog import log
#from .models import Stwdaycount
import json,time,requests
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

getStwInfo = Blueprint('getStwInfo', __name__)

def getTraceId():
  import uuid
  return str(uuid.uuid1()).replace('-', '')

@getStwInfo.route('/bigdata/product_stw/getstwinfo', methods=['POST','GET'])  # 指定接口访问的路径，支持什么请求方式get，post
def get_stwinfo():
    if request.method == 'POST':
        # userid = request.args.get('userid') #使用request.args.get方式获取拼接的入参数据
        schoolid = request.json.get('schoolid')  # 获取带json串请求的userid参数传入的值
        starttime = request.json.get('starttime', int(time.time()) - 24*60*60*8)
        endedtime = request.json.get('endedtime', int(time.time()))
        bookid = request.json.get('bookid','%')
        classid = request.json.get('classid',0)
        gettype = request.json.get('gettype',0)
        subjectname = request.json.get('subjectname','subname')
    # userid = request.values.get('userid') #支持获取连接拼接的参数，而且还能获取body form填入的参数
    if request.method == 'GET':
        return jsonify({'Msg': "Error.You should change the Method to 'Post'!", 'Code': 405, })
    if gettype == 'getbookid':
        s = Getbookid(schoolid)
    elif gettype == 'getstudent':
        s = GetstwStudent(schoolid, starttime, endedtime, subjectname, classid)
    else:
        s = Getstwinfo(schoolid, starttime, endedtime, bookid, classid)
    return jsonify(s.main())
        #json.dumps(s.main(), ensure_ascii=False)

@getStwInfo.route('/bigdata/product_stw/stwInfoHp/clearCache', methods=['GET'])
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
        if not self.classid or self.classid == '' or self.classid == 0:
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
            datas = [x for x in data_list][0][0]
            return datas
        else:
            return 0

    def getkinginfo(self):
        # 数据拉取的主函数
        @cache.memoize(timeout=3000)
        def get_live_hp(schoolIds, classIds):
            # 调取业务实时数据接口，取得数据
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
                cache.delete_memoized('get_live_hp', schoolIds, classIds)
            return reqdatas

        descnames = ['userid', 'username', 'schoolid', 'schoolname', 'classname', 'classid',
                     'bookname', 'bookid', 'hp', 'credit', 'countscore', 'numhomework', 'numselfwork',
                     'topicnum', 'countright', 'rightlv', 'counttime', 'datetime']
        if self.classid is None or self.classid == ''or self.classid == 0:
            sqlsel = "select * from product_stw_daycount where schoolid in (%s) \
                and (unix_timestamp(`datetime`)>=%s and unix_timestamp(`datetime`)<=%s) \
                and bookid like '%s' order by `datetime` DESC " % (
            self.schoolid, self.starttime, self.endedtime, self.bookid)
        else:
            sqlsel = "select * from product_stw_daycount where schoolid in (%s) \
                and (unix_timestamp(`datetime`)>=%s and unix_timestamp(`datetime`)<=%s) \
                and classid in (%s) and bookid like '%s' order by `datetime` DESC " % (
            self.schoolid, self.starttime, self.endedtime, self.classid, self.bookid)
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
                            if dataf[z][descnames[i]] == None:
                                dataf[z][descnames[i]] = 0
                            num[i - 11] += dataf[z][descnames[i]]
                            rdata[descnames[i]] = num[i - 11]
                        else:
                            if rdata[descnames[13]] == 0:
                                rdata[descnames[15]] = rdata[descnames[16]] = 0
                            else:
                                rdata[descnames[15]] = int((rdata[descnames[14]] / rdata[descnames[13]]) * 1000) / 10
                                rdata[descnames[16]] = int((rdata[descnames[16]] / rdata[descnames[13]]) * 10) / 10
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
                            if dataf[z][descnames[i]] == None:
                                dataf[z][descnames[i]] = 0
                            num[i - 11] += dataf[z][descnames[i]]
                            rdata[descnames[i]] = num[i - 11]
                        else:
                            if rdata[descnames[13]] == 0:
                                rdata[descnames[15]] = rdata[descnames[16]] = 0
                            else:
                                rdata[descnames[13]] = rdata[descnames[13]]/10
                                rdata[descnames[15]] = int((rdata[descnames[15]] / len(dataf)) * 100) / 100
                                rdata[descnames[16]] = int((rdata[descnames[16]] / rdata[descnames[13]]) * 10) / 10
                rdatafin.append(rdata)
        reqdatas=get_live_hp(self.schoolid,self.classid)
        allmesses = self.get_all_user()
        findescnames = ['countscore', 'numhomework', 'numselfwork', 'topicnum', 'countright', 'rightlv', 'counttime']
        alldatas = []
        for allmess in allmesses:
            for rdataf in rdatafin:
                if rdataf["userid"] == int(allmess["userid"]):
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
            alldatas.append(allmess)
        lastdatas = []
        for adatas in alldatas:
            for reqdata in reqdatas:
                if reqdata["studentId"] == int(adatas["userid"]):
                    adatas["hp"] = reqdata["hp"]
                    adatas["credit"] = reqdata["credit"]
            if len(adatas) == len(self.alldescs) + len(findescnames):
                adatas["credit"] = adatas["hp"] = 0
            adatas['bookname'] = rdatafin[0]['bookname']
            lastdatas.append(adatas)
        return lastdatas

    def main(self):
        #  判定有学校ID和对应的书本id后，再执行数据拉取，并写入日志
        self.checkschoolid()
        self.checkbookid()
        traceId=getTraceId()
        data = {}
        data['traceId']= traceId
        if self.checkscid == 'right' and self.checkBookid == 'right':
            data['code'] = 200
            data['data'] = Getstwinfo.getkinginfo(self)
            data['msg'] = 'Successful!'
        else:
            data['code'] = 400
            data['msg'] = 'These schools or books are not exist!'
        logInfo = str(data['code'])  + '[' + traceId + ']type[getStwinfo]' + 'scid[' + self.schoolid + ']'\
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
        data_list  = db.session.execute(sqlsel)
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
        traceId=getTraceId()
        data = {}
        data['traceId'] = traceId
        data['code'] = 200
        data['data'] = datav
        data['msg'] = 'successful!'
        logInfo = str(data['code'])+'['+ traceId + ']type[getBookid]' + 'scid[All]'
        log('APIRequest-', logInfo)
        # log('logInfo:Getbookid - ', data['code'])
        return data

class GetstwStudent(object):
    def __init__(self,schoolid, starttime, endedtime, subjectname , classid):
        subpart={"语文":1,"数学":2,"英语":3,"科学":4,"历史":5,"道德与法治":6,"物理":7,}
        self.subjectname = subjectname
        self.schoolid = str(schoolid)
        self.starttime = starttime
        self.endedtime = endedtime
        self.subjectid = subpart.get(self.subjectname)
        self.classid = classid
        self.checkclid = ''
        self.alldescs = ['userid','username']

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

        descnames=['userid','username','topicnum','rightnum']
        sql="SELECT userid,username,SUM(topicnum)AS `topicnum`,sum(countright)AS rightnum FROM product_stw_subcount WHERE classid = %s " \
            "AND subjectid = %s AND unix_timestamp(`datetime`)>=%s and unix_timestamp(`datetime`)<=%s GROUP BY userid,username"\
            %(self.classid,self.subjectid,self.starttime,self.endedtime)
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
                if rdataf["userid"] == int(allmess["userid"]):
                    allmess["username"] = rdataf["username"]
                    allmess["topicnum"] = rdataf["topicnum"]
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
                messa = 'successful!'
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

@getStwInfo.route('/bigdata/product_stw/getid', methods=['GET'])
@cache.cached(timeout=10,key_prefix='view_%s',unless=None)
def getid():
    print("cachetest")
    return jsonify({'test success': 1131231})

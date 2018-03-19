# 0316-实时数据接口重构，加入缓存机制
# 0315-增加全量数据，接口调取时的内部计算，优化处理速度
# 0313-日志结构变更，规范标题大小写
# 0307-增加HP等字段的实时调用接口

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

@getStwInfo.route('/bigdata/product_stw/getstwinfo', methods=['post'])  # 指定接口访问的路径，支持什么请求方式get，post
def get_stwinfo():
    # userid = request.args.get('userid') #使用request.args.get方式获取拼接的入参数据
    schoolid = request.json.get('schoolid')  # 获取带json串请求的userid参数传入的值
    starttime = request.json.get('starttime')
    endedtime = request.json.get('endedtime')
    bookid = request.json.get('bookid',0)
    classid = request.json.get('classid',0)
    gettype = request.json.get('gettype',0)
    # userid = request.values.get('userid') #支持获取连接拼接的参数，而且还能获取body form填入的参数
    if starttime is None or starttime == 0:
        starttime = int(time.time()) - 24*60*60*8
    if endedtime is None or endedtime == 0:
        endedtime = int(time.time())
    if bookid is None or bookid == 0:
        bookid = '%'
    if gettype == 'getbookid':
        s = Getbookid(schoolid)
    else:
        s = Getstwinfo(schoolid, starttime, endedtime, bookid, classid)
    return jsonify(s.main())
        #json.dumps(s.main(), ensure_ascii=False)

class Getstwinfo(object):
    def __init__(self, schoolid, starttime, endedtime, bookid, classid):
        self.schoolid = str(schoolid)
        self.starttime = starttime
        self.endedtime = endedtime
        self.bookid = bookid
        self.classid = classid
        self.checkscid = ''
        self.alldescs = ['userid', 'username', 'schoolid', 'classname']

    def checkschoolid(self): 
        # 检查学校ID是否存在
        sql = "select distinct schoolid from product_stw_daycount where schoolid in (%s) \
                and (unix_timestamp(`datetime`)>=%s and unix_timestamp(`datetime`)<=%s)" % (
        self.schoolid, self.starttime, self.endedtime)
        rs = db.session.execute(sql)
        if len([chrs for chrs in rs ])>0:
            self.checkscid = 'right'

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

    def getkinginfo(self):
        # 数据拉取的主函数
        @cache.memoize(timeout=3000)
        def get_live_hp(schoolIds, classIds):
            # 调取业务实时数据接口，取得数据备用
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
            return reqdatas

        descnames = ['userid', 'username', 'schoolid', 'schoolname', 'classname', 'classid',
                     'bookname', 'bookid', 'hp', 'credit', 'countscore', 'numhomework', 'numselfwork',
                     'topicnum', 'countright', 'rightlv', 'counttime', 'datetime']
        if self.classid is None or self.classid == ''or self.classid == 0:
            sqlsel = "select * from product_stw_daycount where schoolid in (%s) \
                and (unix_timestamp(`datetime`)>=%s and unix_timestamp(`datetime`)<=%s) \
                and bookid like '%s' order by `datetime` DESC " % (
            self.schoolid, self.starttime, self.endedtime, self.bookid)
            getdata = {"schoolIds": self.schoolid, "password": "king123456", }
        else:
            sqlsel = "select * from product_stw_daycount where schoolid in (%s) \
                and (unix_timestamp(`datetime`)>=%s and unix_timestamp(`datetime`)<=%s) \
                and classid in (%s) and bookid like '%s' order by `datetime` DESC " % (
            self.schoolid, self.starttime, self.endedtime, self.classid, self.bookid)
            getdata = {"schoolIds": self.schoolid, "classIds": self.classid, "password": "king123456", }
        data_list  = db.session.execute(sqlsel)
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
        #  判定有学校ID后，再执行数据拉取，并写入日志
        Getstwinfo.checkschoolid(self)
        traceId=getTraceId()
        data = {}
        data['traceId']= traceId
        if self.checkscid == 'right':
            data['code'] = 200
            data['data'] = Getstwinfo.getkinginfo(self)
            data['msg'] = 'successful!'
        else:
            data['code'] = 400
            data['msg'] = 'These schools is not exist!'
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


@getStwInfo.route('/bigdata/product_stw/getid', methods=['GET'])
@cache.cached(timeout=10,key_prefix='view_%s',unless=None)
def getid():
    print("cachetest")
    return jsonify({'test success':1131231})
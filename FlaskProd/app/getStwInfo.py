# 0315-增加全量数据，接口调取时的内部计算
# 0313-日志结构变更，规范标题大小写
# 0307-增加HP等字段的实时调用接口

from flask import Blueprint, render_template, redirect,request
from app import app
from .relog import log
#from .models import Stwdaycount
import json,time,requests,uuid
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

getStwInfo = Blueprint('getStwInfo',__name__)

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
    traceId = str(uuid.uuid1()).replace('-', '')
    if starttime is None or starttime == 0:
        starttime = int(time.time()) - 24*60*60*8
    if endedtime is None or endedtime == 0:
        endedtime = int(time.time())
    if bookid is None or bookid == 0:
        bookid = '%'
    if gettype == 'getbookid':
        s = Getbookid(schoolid,traceId)
    else:
        s = Getstwinfo(schoolid, starttime, endedtime, bookid, classid, traceId)
    return json.dumps(s.main(), ensure_ascii=False)

class Getstwinfo(object):
    def __init__(self, schoolid, starttime, endedtime, bookid, classid, traceId):
        self.schoolid = str(schoolid)
        self.starttime = starttime
        self.endedtime = endedtime
        self.bookid = bookid
        self.classid = classid
        self.checkscid = ''
        self.traceId=traceId
        self.alldescs = ['userid', 'username', 'schoolid', 'classname']

    def checkschoolid(self):
        sql = "select distinct schoolid from product_stw_daycount where schoolid in (%s) \
                and (unix_timestamp(`datetime`)>=%s and unix_timestamp(`datetime`)<=%s)" % (
        self.schoolid, self.starttime, self.endedtime)
        rs = db.session.execute(sql)
        if len([chrs for chrs in rs ])>0:
            self.checkscid = 'right'

    def get_all_user(self):
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
        url = 'http://127.0.0.1:18889/student/studentInfo'
        try:
            reqdatas = requests.get(url, params=getdata).json()
        except:
            reqdatas=[]
        allmesses = self.get_all_user()
        findescnames = ['countscore', 'numhomework', 'numselfwork', 'topicnum', 'countright', 'rightlv', 'counttime']
        alldatas = []
        for allmess in allmesses:
            for reqdata in reqdatas:
                for rdataf in rdatafin:
                    if reqdata["studentId"] == int(allmess["userid"]):
                        allmess["hp"] = reqdata["hp"]
                        allmess["credit"] = reqdata["credit"]
                    if rdataf["userid"] == int(allmess["userid"]):
                        allmess["countscore"] = rdataf["countscore"]
                        allmess["numhomework"] = rdataf["numhomework"]
                        allmess["numselfwork"] = rdataf["numselfwork"]
                        allmess["topicnum"] = rdataf["topicnum"]
                        allmess["countright"] = rdataf["countright"]
                        allmess["rightlv"] = rdataf["rightlv"]
                        allmess["counttime"] = rdataf["counttime"]
            if len(allmess) == len(self.alldescs):
                allmess["credit"] = allmess["hp"] = 0
            if len(allmess) == len(self.alldescs) + 2:
                for findena in findescnames:
                    allmess[findena] = 0
            alldatas.append(allmess)

        return alldatas

    def main(self):
        Getstwinfo.checkschoolid(self)
        data = {}
        data['traceId']= self.traceId
        if self.checkscid == 'right':
            data['code'] = 200
            data['data'] = Getstwinfo.getkinginfo(self)
            data['msg'] = 'successful!'
        else:
            data['code'] = 400
            data['msg'] = 'These schools is not exist!'
        logInfo = str(data['code'])  + '[' + self.traceId + ']type[getStwinfo]' + 'scid[' + self.schoolid + ']'\
                  + 'sttime[' + str(self.starttime) + ']' + 'endtime[' + str(self.endedtime) + ']' + 'bkid[' +\
                str(self.bookid) + ']' + 'clid[' + str(self.classid) + ']'
        log('APIRequest-', logInfo)
        return data

class Getbookid(object):
    def __init__(self, schoolid, traceId):
        self.schoolid = schoolid
        self.traceId = traceId

    def findallbookid(self):
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
        data = {}
        data['traceId'] = self.traceId
        data['code'] = 200
        data['data'] = datav
        data['msg'] = 'successful!'
        logInfo = str(data['code'])+'['+self.traceId + ']type[getBookid]' + 'scid[All]'
        log('APIRequest-', logInfo)
        # log('logInfo:Getbookid - ', data['code'])
        return data



@getStwInfo.route('/bigdata/product_stw/getid', methods=['GET'])
def getid():
    return 'test success'

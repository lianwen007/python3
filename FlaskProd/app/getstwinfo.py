from flask import Blueprint, render_template, redirect,request
from app import app
from .relog import log
#from .models import Stwdaycount
import json,time
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
getstwinfo = Blueprint('getstwinfo',__name__)

@getstwinfo.route('/bigdata/product_stw/getstwinfo', methods=['post'])  # 指定接口访问的路径，支持什么请求方式get，post
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
        if schoolid:
            logInfogetbk =  'type[' + str(gettype) + ']' + 'scid['+schoolid+']'
        else:
            logInfogetbk =  'type[' + str(gettype) + ']' + 'scid[All]'
    else:
        s = Getstwinfo(schoolid, starttime, endedtime, bookid, classid)
        logInfogetbk= 'type[getinfo]' + 'scid['+schoolid+']'
    logInfo=logInfogetbk+'sttime['+str(starttime)+']'+'endtime['+str(endedtime)+']' +'bkid['+str(bookid)+']'+'clid['+str(classid)+']'
    #log('logInfo:APIRequest - ', logInfo)
    return json.dumps(s.main(), ensure_ascii=False)

class Getstwinfo(object):
    def __init__(self, schoolid, starttime, endedtime, bookid, classid):
        self.schoolid = str(schoolid)
        self.starttime = starttime
        self.endedtime = endedtime
        self.bookid = bookid
        self.classid = classid
        self.checkscid = ''

    def checkschoolid(self):
        sql = "select distinct schoolid from product_stw_daycount where schoolid in (%s) \
                and (unix_timestamp(`datetime`)>=%s and unix_timestamp(`datetime`)<=%s)" % (
        self.schoolid, self.starttime, self.endedtime)
        rs = db.session.execute(sql)
        if len([chrs for chrs in rs ])>0:
            self.checkscid = 'right'

    def getkinginfo(self):
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
        return finad

    def main(self):
        Getstwinfo.checkschoolid(self)
        data = {}
        if self.checkscid == 'right':
            data['code'] = 200
            data['data'] = Getstwinfo.getkinginfo(self)
            data['msg'] = 'successful!'
        else:
            data['code'] = -1
            data['msg'] = 'These schools is not exist!'
        log('logInfo:Getstwinfo - ', data['code'])
        return data

class Getbookid(object):
    def __init__(self, schoolid=None):
        self.schoolid = schoolid
    def findallbookid(self):
        sqlsel = "select distinct bookname,bookid from product_stw_daycount"
        descnames = ['bookname', 'bookid']
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
        if self.schoolid:
            datav = Getbookid.findbookidbysc(self)
        else:
            datav = Getbookid.findallbookid(self)
        data = {}
        data['code'] = 200
        data['data'] = datav
        data['msg'] = 'successful!'
        #log('logInfo:Getbookid - ', data['code'])
        return data
@getstwinfo.route('/bigdata/product_stw/getid', methods=['GET'])
def getid():
    return 'GET METHOD test successful！'

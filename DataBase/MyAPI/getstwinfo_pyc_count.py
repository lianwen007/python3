from flask import Flask,request,make_response
from impala.dbapi import connect
import json,time

app = Flask(__name__)#创建一个服务，赋值给APP
@app.route('/bigdata/product_stw/getstwinfo',methods=['post'])#指定接口访问的路径，支持什么请求方式get，post
def get_ss():
    #userid = request.args.get('userid') #使用request.args.get方式获取拼接的入参数据
    schoolid = request.json.get('schoolid') #获取带json串请求的userid参数传入的值
    starttime = request.json.get('starttime')
    endedtime = request.json.get('endedtime')
    bookid = request.json.get('bookid')
    classname = request.json.get('classname')
    gettype = request.json.get('gettype')
    #userid = request.values.get('userid') #支持获取连接拼接的参数，而且还能获取body form填入的参数
    if starttime is None or starttime == 0:
        starttime = int(time.time())-691200
    if endedtime is None or endedtime == 0:
        endedtime = int(time.time())
    if bookid is None or bookid == 0:
        bookid = '%'
    if gettype == 'getbookid':
        s=Getbookid(schoolid)
    else:
        s=Getstwinfo(schoolid,starttime,endedtime,bookid,classname)
    return json.dumps(s.main() , ensure_ascii=False)

@app.route('/bigdata/product_stw/jsontocsv',methods=['post'])
def get_userinfo():
    stwdata=request.values.get('stwdata')
    #schoolid = str(request.json.get('schoolid')) #获取带json串请求的userid参数传入的值
    s=Tranjsoncsv(stwdata)#(str(stwdata))
    content=s.jsontocsv()
    response = make_response(content)
    response.headers["Content-Type"] ="text/html; charset=gb2312"
    response.headers["Content-Disposition"] = "attachment; filename=Stwdata.csv;"

    return response
#conne=connect(host='172.16.10.141', port=21050,timeout=3600) #生产环境
conne=connect(host='bigdata03.yunzuoye.net', port=6667,timeout=3600) #开发环境
class Getstwinfo(object):
    def __init__(self,schoolid,starttime,endedtime,bookid,classname):
        self.schoolid=str(schoolid)
        self.starttime=starttime
        self.endedtime=endedtime
        self.bookid=bookid
        self.classname=classname
        self.conn=conne
        self.checkscid=''

    def checkschoolid(self):
        sql="select distinct schoolid from xh_basecount.product_stw_daycount where schoolid in (%s) \
                and (unix_timestamp(`datetime`)>=%s and unix_timestamp(`datetime`)<=%s)"%(self.schoolid,self.starttime,self.endedtime)
        cur = self.conn.cursor()
        cur.execute(sql)
        rs=cur.fetchall()
        if len(rs)>0:
            self.checkscid='right'

    def getkinginfo(self):
        descnames=['userid','username','schoolid','schoolname','classname','classid',
        'bookname','bookid','hp','credit','countscore','numhomework','numselfwork',
        'topicnum','countright','rightlv','counttime','datetime']
        if self.classname is None or self.classname == '':
            sqlsel="select * from xh_basecount.product_stw_daycount where schoolid in (%s) \
                and (unix_timestamp(`datetime`)>=%s and unix_timestamp(`datetime`)<=%s) \
                and bookid like '%s' order by `datetime` DESC "%(self.schoolid,self.starttime,self.endedtime,self.bookid)
        else:
            sqlsel="select * from xh_basecount.product_stw_daycount where schoolid in (%s) \
                and (unix_timestamp(`datetime`)>=%s and unix_timestamp(`datetime`)<=%s) \
                and classname in (%s) and bookid like '%s' order by `datetime` DESC "%(self.schoolid,self.starttime,self.endedtime,self.classname,self.bookid)
        cur = self.conn.cursor()
        cur.execute(sqlsel)
        messes,mesind,finad=[],[],[]
        rdatafin=[]
        data_list=cur.fetchall()
        for datas in data_list:
            mess={}
            for x in range(len(datas)):
                mess[descnames[x]]=datas[x]
            messes.append(mess)
        for mes in messes:
            mesind.append(mes['userid'])
        mesindex=list(set(mesind))
        for y in mesindex:
            #findata=[]
            dataz=[]
            for mes in messes:
                if mes['userid']==y:
                    dataz.append(mes)
            #findata.append(dataz)
            finad.append(dataz)
        for dataf in finad:
            rdata={}
            for z in range(len(dataf)):
                for i in range(len(dataf[z])):
                    num=0
                    if i<=9:
                        rdata[descnames[i]]=dataf[0][descnames[i]]
                    elif i<=16:
                        if dataf[z][descnames[i]]==None:
                            dataf[z][descnames[i]]=0
                        num=num+dataf[z][descnames[i]]
                        rdata[descnames[i]]=num
                    else:
                        if rdata[descnames[13]]==0:
                            rdata[descnames[15]]=0
                            rdata[descnames[16]]=0
                        else:
                            rdata[descnames[15]]=rdata[descnames[14]]/rdata[descnames[13]]
                            rdata[descnames[16]]=rdata[descnames[16]]/rdata[descnames[13]]
            rdatafin.append(rdata)
        return rdatafin
    def main(self):
        Getstwinfo.checkschoolid(self)
        data={}
        if self.checkscid=='right':
            data['code']=200
            data['data']=Getstwinfo.getkinginfo(self)
            data['msg']='successful!'
        else:
            data['code']=-1
            data['msg']='These schools is not exist!'
        return data

class Tranjsoncsv(object):
    def __init__(self,jsonstr):
        self.jsonstr=jsonstr

    def jsontocsv(self):
        val,val2='',''
        valuename=['schoolid','schoolname','bookname','classname','username','hp','credit','countscore','numhomework','numselfwork','topicnum','countright','rightlv','counttime']
        valuenamechn=['学校ID','学校名称','书名','班级','姓名','体力','诚信分','积分','作业次数','自练次数','做题量','正确地梁','正确率','平均做题时间(秒)']
        jsonvalues=json.loads(str(self.jsonstr))
        #for keyname in jsonvalues[0].keys():
        #    data.append(keyname)    
        for vals in jsonvalues:
            data=[]
            for x in valuename:
                data.append(str(vals[x]))
            val=','.join(data)
            val2=val2+val+'\n'
            datav = ','.join(valuenamechn)+'\n'+val2
        return datav.encode('gb2312')

class Getbookid(object):
    def __init__(self,schoolid=None):
        self.schoolid=schoolid
        self.conn=conne
    def findallbookid(self):
        sqlsel="select distinct bookname,bookid from xh_basecount.product_stw_daycount"
        descnames=['bookname','bookid']
        cur = self.conn.cursor()
        cur.execute(sqlsel)
        data_list=cur.fetchall()
        messes=[]
        for datas in data_list:
            mess={}
            for x in range(len(datas)):
                mess[descnames[x]]=datas[x]
            messes.append(mess)
        return messes
    def findbookidbysc(self):
        sqlsel="select distinct bookname,bookid from xh_basecount.product_stw_daycount where schoolid in (%s)"%(self.schoolid)
        descnames=['bookname','bookid']
        cur = self.conn.cursor()
        cur.execute(sqlsel)
        data_list=cur.fetchall()
        messes=[]
        for datas in data_list:
            mess={}
            for x in range(len(datas)):
                mess[descnames[x]]=datas[x]
            messes.append(mess)
        return messes
    def main(self):
        if self.schoolid:
            datav=Getbookid.findbookidbysc(self)
        else:
            datav=Getbookid.findallbookid(self)
        data={}
        data['code']=200
        data['data']=datav
        data['msg']='successful!'
        return data

app.run(host='0.0.0.0',port=9998,debug=False,threaded=True)


#from impala.dbapi import connect
#from impala.util import as_pandas
#conn = connect(host='10.161.20.11', port=21050)
#cur = conn.cursor()
#cur.execute('SHOW TABLES')
#cur.execute('SELECT * FROM businfo')
#data = as_pandas(cur)
#print (data)
#print (type(data))
#'schoolid','schoolname','bookname','classname','username','hp','credit','countscore','numhomework','numselfwork','topicnum','countright','rightlv','counttime'     导出接口需要的POST字段

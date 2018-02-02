# -*- coding: utf-8 -*-
#20180202-Update 增加schoolid检查，若无则返回错误信息
"""
Created on Thu Feb  1 20:45:56 2018

@author: Administrator
"""
from flask import Flask,request
from impala.dbapi import connect
import json

app = Flask(__name__)#创建一个服务，赋值给APP
@app.route('/bigdata/product_stw/getstwinfo',methods=['post'])#指定接口访问的路径，支持什么请求方式get，post
def get_ss():
    #userid = request.args.get('userid') #使用request.args.get方式获取拼接的入参数据
    schoolid = str(request.json.get('schoolid')) #获取带json串请求的userid参数传入的值
    starttime = request.json.get('starttime')
    endedtime = request.json.get('endedtime')
    #userid = request.values.get('userid') #支持获取连接拼接的参数，而且还能获取body form填入的参数
    s=Getstwinfo(schoolid,starttime,endedtime)
    return json.dumps(s.main() , ensure_ascii=False)


class Getstwinfo(object):
    def __init__(self,schoolid,starttime,endedtime):
        self.schoolid=str(schoolid)
        self.starttime=starttime
        self.endedtime=endedtime
        self.conn=connect(host='172.16.10.141', port=21050,timeout=3600)
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
        sqlsel="select * from xh_basecount.product_stw_daycount where schoolid in (%s) \
                and (unix_timestamp(`datetime`)>=%s and unix_timestamp(`datetime`)<=%s)"%(self.schoolid,self.starttime,self.endedtime)
        cur = self.conn.cursor()
        cur.execute(sqlsel)
        messes=[]
        data_list=cur.fetchall()
        for datas in data_list:
            mess={}
            for x in range(len(datas)):
                mess[descnames[x]]=datas[x]
            messes.append(mess)
        return messes
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

app.run(host='172.16.20.222',port=18890,debug=True,threaded=True)

# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 09:24:35 2018

@author: Administrator
"""
from flask import Flask,request,make_response
from impala.dbapi import connect
import json,time,pymysql,requests
#
#class Getbookid(object):
#    def __init__(self,schoolid=None):
#        self.schoolid=schoolid
#        self.conn=connect(host='bigdata03.yunzuoye.net', port=6667,timeout=3600)
#    def findallbookid(self):
#        sqlsel="select distinct bookname,bookid from xh_basecount.product_stw_daycount"      
#        descnames=['bookname','bookid']             
#        cur = self.conn.cursor()
#        cur.execute(sqlsel)
#        data_list=cur.fetchall()
#        messes=[]
#        for datas in data_list:
#            mess={}
#            for x in range(len(datas)):
#                mess[descnames[x]]=datas[x]
#            messes.append(mess)
#        return messes
#    def findbookidbysc(self):
#        sqlsel="select distinct bookname,bookid from xh_basecount.product_stw_daycount where schoolid in (%s)"%(self.schoolid)
#        descnames=['bookname','bookid']             
#        cur = self.conn.cursor()
#        cur.execute(sqlsel)
#        data_list=cur.fetchall()
#        messes=[]
#        for datas in data_list:
#            mess={}
#            for x in range(len(datas)):
#                mess[descnames[x]]=datas[x]
#            messes.append(mess)
#        return messes        
#    def main(self):
#        if self.schoolid: 
#            datav=Getbookid.findbookidbysc(self)
#        else:
#            datav=Getbookid.findallbookid(self)
#        data={}
#        data['code']=200
#        data['data']=datav
#        data['msg']='successful!'
#        return data
#
#s=Getbookid('760')
#print(s.main())

schoolid='760'
starttime=int(time.time())-6912000
endedtime=int(time.time())
bookid=''
classid='%'
#conn=connect(host='bigdata03.yunzuoye.net', port=6667,timeout=3600)
conn=pymysql.connect(host="localhost",port=3306,user="root",passwd="123",db="elasticsearch",charset="utf8") #开发环境
#if schoolid is None or schoolid == '':    
#    sqlsel="select distinct bookname,bookid from xh_basecount.product_stw_daycount "
#else:
#    sqlsel="select distinct bookname,bookid from xh_basecount.product_stw_daycount where schoolid in (%s)"%(schoolid)     
#descnames=['bookname','bookid']             
#cur = conn.cursor()
#cur.execute(sqlsel)
#data_list=cur.fetchall()
#messes=[]
#for datas in data_list:
#    mess={}
#    for x in range(len(datas)):
#        mess[descnames[x]]=datas[x]
#    messes.append(mess)
#checkscid=''

descnames=['userid','username','schoolid','schoolname','classid','classid',
'bookname','bookid','hp','credit','countscore','numhomework','numselfwork',
'topicnum','countright','rightlv','counttime','datetime']
if bookid is None or bookid == '':    
    sqlsel="select * from product_stw_daycount where schoolid in (%s) \
        and (unix_timestamp(`datetime`)>=%s and unix_timestamp(`datetime`)<=%s) \
        and classid like '%s' order by `datetime` "%(schoolid,starttime,endedtime,classid)
else:
    sqlsel="select * from product_stw_daycount where schoolid in (%s) \
        and (unix_timestamp(`datetime`)>=%s and unix_timestamp(`datetime`)<=%s) \
        and classid like '%s' and bookid in (%s) order by `datetime`"%(schoolid,starttime,endedtime,classid,bookid)
cur = conn.cursor()
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
if classid == '%' or classid is None:
    getdata={"schoolIds":schoolid,"password":"king123456",}
else:
    getdata={"classIds":classid,"password":"king123456",}
url = 'http://192.168.8.53:18889/student/studentInfo'
reqdatas =requests.get(url, params=getdata).json()
if requests.get(url, params=getdata).json()!=[]:
    zdatas=[]
    for xdata in messes:
        for reqdata in reqdatas:
            if reqdata["studentId"]==xdata["userid"]:
                xdata["hp"]=reqdata["hp"]
                xdata["credit"]=reqdata["credit"]
        zdatas.append(xdata)    
else:
    zdatas=messes
for y in mesindex:
    dataz=[]
    for mes in zdatas:
        if mes['userid']==y:
            dataz.append(mes)
    finad.append(dataz)
print(finad[0])
#for dataf in finad:
#    rdata={}
#    for z in range(len(dataf)): 
#        for i in range(len(dataf[z])):
#            num=0
#            if i<=9:
#                rdata[descnames[i]]=dataf[0][descnames[i]]
#            elif i<=16:
#                if dataf[z][descnames[i]]==None:
#                    dataf[z][descnames[i]]=0
#                num=num+dataf[z][descnames[i]]
#                rdata[descnames[i]]=num          
#            else:
#                if rdata[descnames[13]]==0:
#                    rdata[descnames[15]]=0
#                    rdata[descnames[16]]
#                else:
#                    rdata[descnames[15]]=rdata[descnames[14]]/rdata[descnames[13]]
#                    rdata[descnames[16]]=rdata[descnames[16]]/rdata[descnames[13]]
#    rdatafin.append(rdata)
     

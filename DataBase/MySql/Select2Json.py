# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 09:33:22 2018

@author: Administrator
"""
import pymysql
import json

db=pymysql.connect(host="localhost",port=3306,user="root",passwd="123",db="elasticsearch",charset="utf8")
cursor=db.cursor()
userid=52919
sql="SELECT * FROM user_file_product WHERE userid = %d"%(userid)

try:
    cursor.execute(sql)
    results=cursor.fetchone()
except:
    print("Error")
db.close()

"""mess={'id':0,
      'userid':0,
      'username':'',
      'schoolid':0,
      'schoolname':'',
      'gradename':'',
      'scorestatus':0,
      'scorechn':0.0,
      'rankchn':0.0,
      'scoremath':0.0,
      'rankmath':0.0,
      'scoreeng':0.0,
      'rankeng':0.0,
      'scoresci':0.0,
      'ranksci':0.0,
      'avgstatus':0,
      'topstatus':0,
      'topnumber':0.0,
      'finalstatus':0,
      'datetime':0 
      }"""
mess={}      
mess['id']=results[0]
mess['userid']=results[1]
mess['username']=results[2]
mess['schoolid']=results[3]
mess['schoolname']=results[4]
mess['gradename']=results[5]
mess['scorestatus']=results[6]
mess['scorechn']=results[7]
mess['rankchn']=results[8]
mess['scoremath']=results[9]
mess['rankmath']=results[10]
mess['scoreeng']=results[11]
mess['rankeng']=results[12]
mess['scoresci']=results[13]
mess['ranksci']=results[14]
mess['avgstatus']=results[15]
mess['topstatus']=results[16]
mess['topnumber']=results[17]
mess['finalstatus']=results[18]
mess['datetime']=results[19]
jsonstr=json.dumps(mess)
print(jsonstr)

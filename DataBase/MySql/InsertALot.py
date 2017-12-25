# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 14:58:02 2017

@author: Administrator
"""


import pymysql
import random
import datetime


db=pymysql.connect(host="localhost",port=3306,user="root",passwd="123",db="hadoop",charset="utf8")
cursor=db.cursor()
sql="insert into school_grade_user values(%s,%s,%s,%s,%s,%s,%s,%s)"
ndate=datetime.datetime.now() + datetime.timedelta(days=-1)

try:
    for i in range(100):
        x=str(random.randint(0,1000))
        y=str(random.randint(0,15))
        z=str(random.randint(0,5))
        cursor.execute(sql,(x,x,y,y,z,'0','0',ndate.strftime('%Y-%m-%d')))
        db.commit()
except:
    print("Error")
db.close()


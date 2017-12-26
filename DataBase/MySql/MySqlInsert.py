# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 16:37:00 2017

@author: Alian
"""

import pymysql

db=pymysql.connect(host="localhost",port=3306,user="root",passwd="123",db="elasticsearch",charset="utf8")
cursor=db.cursor()
sql="""insert into test02(
SELECT * FROM test01)"""

try:
    cursor.execute(sql)
    db.commit()
except:
    print("Error")
db.close()  



# select操作并打印数据 
info = cur.fetchmany(aa)
for ii in info:
    print ii

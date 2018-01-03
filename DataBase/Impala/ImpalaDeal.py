# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 08:55:47 2018

@author: Administrator
"""
from impala.dbapi import connect


conn = connect(host='192.168.0.10', port=21050)
cur = conn.cursor()
cur.execute('select name as num from user ;')
data_list=cur.fetchall()
for data in data_list:
    #用户列表
   print ("用户名称:",data)

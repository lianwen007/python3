# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 09:53:44 2018

@author: Administrator
"""
from flask import Flask,request
import pymysql
import json
#平均耗时2.05s

tablename='user_file_product'

app = Flask(__name__)#创建一个服务，赋值给APP
@app.route('/bigdata/user_file_product/getuserid',methods=['get'])#指定接口访问的路径，支持什么请求方式get，post
def get_ss():
    userid = request.args.get('userid') #使用request.args.get方式获取拼接的入参数据
    #userid = request.json.get('userid') #获取带json串请求的userid参数传入的值
    #userid = request.values.get('userid') #支持获取连接拼接的参数，而且还能获取body form填入的参数
    data=get_mysql_conn(userid)
    return data

    
def get_mysql_desc():
    """查询数据库表的字段名称，传入参数备用"""
    db2=pymysql.connect(host="localhost",port=3306,
                       user="root",passwd="123",db="elasticsearch",charset="utf8")
    cursor2=db2.cursor()
    sqldesc="DESC " + tablename
    #mysqldescs=[]
    try:
        cursor2.execute(sqldesc)
        descnames = cursor2.fetchall()
        mysqldescs=[descname[:][0] for descname in descnames]
        #for descname in descnames:
            #mysqldesc=descname[:][0]
            #mysqldescs.append(descname[:][0])
    except:
        'Error'
    db2.close()
    return mysqldescs

def get_mysql_conn(userid=''):
    """根据条件进行查询，将字段名称和字段值对应，产出JSON格式"""
    #userid='60219'
    keywords = 'userid'
    db1=pymysql.connect(host="localhost",port=3306,
                   user="root",passwd="123",db="elasticsearch",charset="utf8")
    cursor1=db1.cursor()
    sql="SELECT * FROM "+ tablename +" WHERE "+ keywords + " = %s"%(userid)
    messnames=get_mysql_desc()
    mess={}
    
    try:
        cursor1.execute(sql)
        result=cursor1.fetchone()
        for x in range(len(result)): #空值处理为0
            if result[x] is not None:
                mess[messnames[x]]=result[x]
            else:
                mess[messnames[x]]=0
    except:
        #'Error'
        mess['error']='Userid '+ userid + ' is not exist!'
    db1.close()
        #print(json.dumps(mess , ensure_ascii=False)) 
    return json.dumps(mess , ensure_ascii=False)

app.run(host='0.0.0.0',port=8802,debug=True)

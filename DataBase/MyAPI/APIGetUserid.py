# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 11:13:52 2018 重构版本

@author: Administrator
"""

from flask import Flask,request
import pymysql
import json
import time

app = Flask(__name__)#创建一个服务，赋值给APP
@app.route('/bigdata/user_file_product/getuserid',methods=['get'])#指定接口访问的路径，支持什么请求方式get，post
def get_ss():
    #start = time.clock()
    userid = request.args.get('userid') #使用request.args.get方式获取拼接的入参数据
    #userid = request.json.get('userid') #获取带json串请求的userid参数传入的值
    #userid = request.values.get('userid') #支持获取连接拼接的参数，而且还能获取body form填入的参数
    s=Getuserfile(userid)
    #elapsed = (time.clock() - start)
    return s.main() #+ str(elapsed)

class Getuserfile(object):
    def __init__(self,userid):
        self.userid=str(userid)
        self.conn=pymysql.connect(host="localhost",port=3306,
                           user="root",passwd="123",db="elasticsearch",charset="utf8")
        self.messnames=Getuserfile.get_mysql_desc(self)
    def get_mysql_desc(self):
        """查询数据库表的字段名称，传入参数备用"""
        cursor=self.conn.cursor()
        sqldesc="DESC user_file_product"
        #mysqldescs=[]
        try:
            cursor.execute(sqldesc)
            descnames = cursor.fetchall()
            mysqldescs=[descname[:][0] for descname in descnames]
            #for descname in descnames:
                #mysqldesc=descname[:][0]
                #mysqldescs.append(descname[:][0])
        finally:
            cursor.close()
        return mysqldescs
    
    def get_mysql_conn(self):
        """根据条件进行查询，将字段名称和字段值对应，产出JSON格式"""
        #userid='60219'
        cursor=self.conn.cursor()
        sql="SELECT * FROM user_file_product WHERE userid = '%s'"%(self.userid)
        mess={}
        try:
            cursor.execute(sql)
            result=cursor.fetchone()
            for x in range(len(result)): #空值处理为0
                if result[x] is not None:
                    mess[self.messnames[x]]=result[x]
                else:
                    mess[self.messnames[x]]=0
        except:
            #'Error'
            mess['error']='Userid '+ self.userid + ' is not exist!'
        cursor.close()
            #print(json.dumps(mess , ensure_ascii=False)) 
        return json.dumps(mess , ensure_ascii=False)
    
    def main(self):
        Getuserfile.get_mysql_desc(self)
        data=Getuserfile.get_mysql_conn(self)
        return data

app.run(host='0.0.0.0',port=8810,debug=True)

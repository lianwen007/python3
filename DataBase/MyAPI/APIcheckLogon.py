# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 09:27:21 2018

@author: Administrator
"""
from flask import Flask,request
import pymysql
import json
import time

app = Flask(__name__)#创建一个服务，赋值给APP
@app.route('/bigdata/getuserinfo',methods=['post'])#指定接口访问的路径，支持什么请求方式get，post
def get_ss():
    #start = time.clock()
    username = request.json.get('username') #使用request.args.get方式获取拼接的入参数据
    pwd = request.json.get('password')
    #username = request.args.get('userid') #使用request.args.get方式获取拼接的入参数据
    #userid = request.json.get('userid') #获取带json串请求的userid参数传入的值
    #userid = request.values.get('userid') #支持获取连接拼接的参数，而且还能获取body form填入的参数
    data=Userlogin(username,pwd)
    #elapsed = (time.clock() - start)
    return json.dumps(data.main() , ensure_ascii=False) #+ str(elapsed) #测试接口调用耗时
    
class Userlogin(object):
    
    def __init__(self,username,password):
        self.username=str(username)
        self.password=password.upper()
        self.conn=pymysql.connect(host="localhost",port=3306,
                           user="root",passwd="123",db="elasticsearch",charset="utf8")
        self.checkuserpoint='wrong'
        self.checkpwdpoint='wrong'
    def checkusername(self):
        #检查用户名是否存在，存在则改变关键字段信息
        cursor=self.conn.cursor()
        try:
            usersql="select * from xhsys_user where sLogonName= '%s'"%(self.username)
            cursor.execute(usersql)
            rs = cursor.fetchall()
            if len(rs) == 1:
                self.checkuserpoint='right'
        finally:
            cursor.close()
    def checkpassword(self):
        #如果用户名正确，检查密码，如果正确则下一步
        cursor=self.conn.cursor()
        if self.checkuserpoint=='right':
            try:
                sqlsel="select sLogonPwd from xhsys_user \
                        where sLogonName = '%s' "%(self.username)
                cursor.execute(sqlsel)
                rs=cursor.fetchall()
                if len(rs) == 1 and str(rs[0][0]).upper()==self.password:
                    self.checkpwdpoint='right'
            finally:
                cursor.close()
    def getuserinfo(self):
        cursor=self.conn.cursor()
        messnames=['userid','logonName','userType','userPhone']
        mess={}
        if self.checkuserpoint=='right' and self.checkpwdpoint=='right':
            try:
                sqlsel="select iUserId,sLogonName,iUserType,sSelfPhone \
                        from xhsys_user where sLogonName = '%s' and upper(sLogonPwd)= '%s' "%(self.username,self.password)
                cursor.execute(sqlsel)
                results=cursor.fetchone()
                if len(results)!=0:
                    for x in range(len(results)):
                        mess[messnames[x]]=results[x]
            finally:
                cursor.close()
        return mess
    def main(self):
        Userlogin.checkusername(self)
        Userlogin.checkpassword(self)
        data={}
        if self.checkuserpoint!='right':
            data['error']='Username '+ self.username + ' is not exist!'
        elif self.checkpwdpoint!='right':
            data['error']='Your password is wrong! Check it please!'
        else:
            data=Userlogin.getuserinfo(self)
        return data

app.run(host='0.0.0.0',port=8808,debug=True)  
     
"""
if __name__=="__main__":
    s=Userlogin('wangziwei','a23b5d3bd4f0d8fa2ec9cef81068d137')
    print (json.dumps(s.main() , ensure_ascii=False))
"""

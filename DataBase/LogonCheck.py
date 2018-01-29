# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 13:27:21 2018

@author: Administrator
"""
import pymysql

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
                rs=cursor.fetchall() #取出密码转为全大写，然后做对比
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
        if self.checkuserpoint!='right':
            data='Username '+ self.username + ' is not exist!'
        elif self.checkpwdpoint!='right':
            data='Your password is wrong! Check it please!'
        else:
            data=Userlogin.getuserinfo(self)
        return data

if __name__=="__main__":
    s=Userlogin('wangziwei','a23b5d3bd4f0d8fa2ec9cef81068d137')
    print(s.main())

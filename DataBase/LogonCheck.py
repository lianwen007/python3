# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 13:27:21 2018

@author: Administrator
"""
import pymysql

class Userlogin(object):
    
    def __init__(self,getType,username,password):
        self.getType=getType
        self.username=username
        self.password=password
        self.conn=pymysql.connect(host="localhost",port=3306,
                           user="root",passwd="123",db="elasticsearch",charset="utf8")
        self.checkuserpoint='wrong'
        self.checkpwdpoint='wrong'
        
    def checkusername(self):
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
        cursor=self.conn.cursor()
        if self.checkuserpoint=='right':
            try:
                sqlsel="select * from xhsys_user \
                        where sLogonName = '%s' and sLogonPwd= '%s' "%(self.username,self.password)
                cursor.execute(sqlsel)
                rs=cursor.fetchall()
                if len(rs) == 1:
                    self.checkpwdpoint='right'
            finally:
                cursor.close()
    def getuserinfo(self):
 
        cursor=self.conn.cursor()
        messnames=['userid','logonName','userType','userPhone']
        mess={}
        try:
            sqlsel="select iUserId,sLogonName,iUserType,sSelfPhone \
                    from xhsys_user where sLogonName = '%s' and sLogonPwd= '%s' "%(self.username,self.password)
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
        if self.checkuserpoint=='wrong':
            data='Username '+ self.username + ' is not exist!'
        
        elif self.checkpwdpoint=='wrong':
            data='Your password  is wrong! Check it please!'
        else:
            data=Userlogin.getuserinfo(self)
        print(data)

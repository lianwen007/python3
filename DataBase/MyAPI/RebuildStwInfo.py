# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 09:19:30 2018

@author: Administrator
"""
#pip install mysql-connector-python-rf
from sqlalchemy import Column,Integer,String,BigInteger,Float, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()
#descnames = ['userid', 'username', 'schoolid', 'schoolname', 'classname', 'classid',
#                 'bookname', 'bookid', 'hp', 'credit', 'countscore', 'numhomework', 'numselfwork',
#                 'topicnum', 'countright', 'rightlv', 'counttime', 'datetime']
# 定义User对象:
class Stwdaycount(Base):
    __tablename__ = 'product_stw_daycount'
    userid = Column(Integer)
    username = Column(String(80))
    schoolid = Column(BigInteger)
    schoolname = Column(String(200))
    classname = Column(String(200))
    classid = Column(Integer)
    bookname = Column(String(200))
    bookid = Column(String(200), primary_key=True)
    hp = Column(Integer, primary_key=True)
    credit = Column(Integer, primary_key=True)
    countscore = Column(Float)
    numhomework = Column(Integer)
    numselfwork = Column(Integer)
    topicnum = Column(Integer)
    countright = Column(Integer)
    rightlv = Column(Float)
    counttime = Column(Integer)
    datetime = Column(String(200), primary_key=True)

# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:123@localhost:3306/elasticsearch')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()
# 创建新User对象:
#new_user = Test01(asd=5, lltest='dddss' , aaa='Bob')
# 添加到session:
#session.add(new_user)
# 提交即保存到数据库:
#p_user=32673
#sql = 'select * from product_stw_daycount where userid=%s limit 0,10'%(p_user)
#items = list()
schoolid='899'
starttime=1517414400
endedtime=1519699289
checkscid = ''
#sql = "select distinct schoolid from product_stw_daycount where schoolid in (%s) \
#        and (unix_timestamp(`datetime`)>=%s and unix_timestamp(`datetime`)<=%s)" % (
#schoolid, starttime, endedtime)
#rs = session.execute(sql)
#a=[{
#   "userid":5522,
#   "username":"asd",
#   "info":123,
#   },{
#   "userid":5522,
#   "username":"asd",
#   "info":456,
#   },
#   {
#    "userid":6644,
#    "username":"aaa",
#    }
#   ]
#b=[{
#    "userid":5522,
#    "hp":123,
#    "credit":111
#    },
#   {
#    "userid":6644,
#    "hp":22,
#    "credit":323
#    }
#   ]
#z=[]
#for x in a:
#    for y in b:
#        if y["userid"]==x["userid"]:
#            x["hp"]=y["hp"]
#            x["credit"]=y["credit"]
#    z.append(x)    
#print(z)
##finrs=
##for chrs in rs:
##    finrs.append(chrs)
#if len([chrs for chrs in rs ])>0:
#    checkscid = 'right'
## 执行sql ，返回值都是list()，要取值遍历，每一个直接通过'.字段名'的方式取指定的字段
#items = session.execute(sql)
##items = session.query(Stwdaycount).filter(Stwdaycount.userid==32673).all()
#for item in items:
#    #for descname in descnames:
#    print(item.counttime)
#    print(len(item))
# 关闭session:
#session.close()
reqdatas=[
  {
    "studentId": 54732,
    "schoolId": 899,
    "classId": 2427,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54829,
    "schoolId": 899,
    "classId": 2430,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54826,
    "schoolId": 899,
    "classId": 2430,
    "hp": 17,
    "credit": 33,
    "grade": 21
  },
  {
    "studentId": 54702,
    "schoolId": 899,
    "classId": 2427,
    "hp": 15,
    "credit": 45,
    "grade": 21
  },
  {
    "studentId": 54790,
    "schoolId": 899,
    "classId": 2429,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54788,
    "schoolId": 899,
    "classId": 2429,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54854,
    "schoolId": 899,
    "classId": 2430,
    "hp": 6,
    "credit": 32,
    "grade": 21
  },
  {
    "studentId": 54846,
    "schoolId": 899,
    "classId": 2430,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54817,
    "schoolId": 899,
    "classId": 2429,
    "hp": 9,
    "credit": -15,
    "grade": 21
  },
  {
    "studentId": 54606,
    "schoolId": 899,
    "classId": 2425,
    "hp": 3,
    "credit": 109,
    "grade": 21
  },
  {
    "studentId": 54641,
    "schoolId": 899,
    "classId": 2425,
    "hp": 15,
    "credit": 17,
    "grade": 21
  },
  {
    "studentId": 54811,
    "schoolId": 899,
    "classId": 2429,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54800,
    "schoolId": 899,
    "classId": 2429,
    "hp": 19,
    "credit": 63,
    "grade": 21
  },
  {
    "studentId": 54696,
    "schoolId": 899,
    "classId": 2427,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54753,
    "schoolId": 899,
    "classId": 2428,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54782,
    "schoolId": 899,
    "classId": 2429,
    "hp": 12,
    "credit": 43,
    "grade": 21
  },
  {
    "studentId": 54610,
    "schoolId": 899,
    "classId": 2425,
    "hp": 20,
    "credit": 108,
    "grade": 21
  },
  {
    "studentId": 54804,
    "schoolId": 899,
    "classId": 2429,
    "hp": 6,
    "credit": 36,
    "grade": 21
  },
  {
    "studentId": 54734,
    "schoolId": 899,
    "classId": 2428,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54806,
    "schoolId": 899,
    "classId": 2429,
    "hp": 13,
    "credit": 40,
    "grade": 21
  },
  {
    "studentId": 54816,
    "schoolId": 899,
    "classId": 2429,
    "hp": 3,
    "credit": 29,
    "grade": 21
  },
  {
    "studentId": 54605,
    "schoolId": 899,
    "classId": 2425,
    "hp": 2,
    "credit": 39,
    "grade": 21
  },
  {
    "studentId": 54635,
    "schoolId": 899,
    "classId": 2425,
    "hp": 7,
    "credit": 180,
    "grade": 21
  },
  {
    "studentId": 54630,
    "schoolId": 899,
    "classId": 2425,
    "hp": 7,
    "credit": 114,
    "grade": 21
  },
  {
    "studentId": 54629,
    "schoolId": 899,
    "classId": 2425,
    "hp": 1,
    "credit": 49,
    "grade": 21
  },
  {
    "studentId": 54689,
    "schoolId": 899,
    "classId": 2427,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54747,
    "schoolId": 899,
    "classId": 2428,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54772,
    "schoolId": 899,
    "classId": 2428,
    "hp": 20,
    "credit": 75,
    "grade": 21
  },
  {
    "studentId": 54739,
    "schoolId": 899,
    "classId": 2428,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54726,
    "schoolId": 899,
    "classId": 2427,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54834,
    "schoolId": 899,
    "classId": 2430,
    "hp": 9,
    "credit": 58,
    "grade": 21
  },
  {
    "studentId": 54831,
    "schoolId": 899,
    "classId": 2430,
    "hp": 7,
    "credit": 38,
    "grade": 21
  },
  {
    "studentId": 54815,
    "schoolId": 899,
    "classId": 2429,
    "hp": 20,
    "credit": 140,
    "grade": 21
  },
  {
    "studentId": 54785,
    "schoolId": 899,
    "classId": 2429,
    "hp": 11,
    "credit": 38,
    "grade": 21
  },
  {
    "studentId": 54763,
    "schoolId": 899,
    "classId": 2428,
    "hp": 6,
    "credit": 39,
    "grade": 21
  },
  {
    "studentId": 54729,
    "schoolId": 899,
    "classId": 2427,
    "hp": 13,
    "credit": 39,
    "grade": 21
  },
  {
    "studentId": 54749,
    "schoolId": 899,
    "classId": 2428,
    "hp": 17,
    "credit": 52,
    "grade": 21
  },
  {
    "studentId": 54699,
    "schoolId": 899,
    "classId": 2427,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54795,
    "schoolId": 899,
    "classId": 2429,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54807,
    "schoolId": 899,
    "classId": 2429,
    "hp": 7,
    "credit": 32,
    "grade": 21
  },
  {
    "studentId": 54597,
    "schoolId": 899,
    "classId": 2425,
    "hp": 20,
    "credit": 155,
    "grade": 21
  },
  {
    "studentId": 54754,
    "schoolId": 899,
    "classId": 2428,
    "hp": 4,
    "credit": 134,
    "grade": 21
  },
  {
    "studentId": 54767,
    "schoolId": 899,
    "classId": 2428,
    "hp": 20,
    "credit": 94,
    "grade": 21
  },
  {
    "studentId": 54748,
    "schoolId": 899,
    "classId": 2428,
    "hp": 18,
    "credit": 82,
    "grade": 21
  },
  {
    "studentId": 54613,
    "schoolId": 899,
    "classId": 2425,
    "hp": 20,
    "credit": 114,
    "grade": 21
  },
  {
    "studentId": 54770,
    "schoolId": 899,
    "classId": 2428,
    "hp": 3,
    "credit": 34,
    "grade": 21
  },
  {
    "studentId": 54830,
    "schoolId": 899,
    "classId": 2430,
    "hp": 14,
    "credit": 111,
    "grade": 21
  },
  {
    "studentId": 54744,
    "schoolId": 899,
    "classId": 2428,
    "hp": 0,
    "credit": 3,
    "grade": 21
  },
  {
    "studentId": 54762,
    "schoolId": 899,
    "classId": 2428,
    "hp": 13,
    "credit": 39,
    "grade": 21
  },
  {
    "studentId": 54771,
    "schoolId": 899,
    "classId": 2428,
    "hp": 20,
    "credit": 78,
    "grade": 21
  },
  {
    "studentId": 54752,
    "schoolId": 899,
    "classId": 2428,
    "hp": 13,
    "credit": 35,
    "grade": 21
  },
  {
    "studentId": 54608,
    "schoolId": 899,
    "classId": 2425,
    "hp": 7,
    "credit": 107,
    "grade": 21
  },
  {
    "studentId": 54637,
    "schoolId": 899,
    "classId": 2425,
    "hp": 2,
    "credit": 239,
    "grade": 21
  },
  {
    "studentId": 54598,
    "schoolId": 899,
    "classId": 2425,
    "hp": 7,
    "credit": 40,
    "grade": 21
  },
  {
    "studentId": 54626,
    "schoolId": 899,
    "classId": 2425,
    "hp": 6,
    "credit": 43,
    "grade": 21
  },
  {
    "studentId": 54627,
    "schoolId": 899,
    "classId": 2425,
    "hp": 20,
    "credit": 121,
    "grade": 21
  },
  {
    "studentId": 54659,
    "schoolId": 899,
    "classId": 2426,
    "hp": 3,
    "credit": 56,
    "grade": 21
  },
  {
    "studentId": 54835,
    "schoolId": 899,
    "classId": 2430,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54774,
    "schoolId": 899,
    "classId": 2428,
    "hp": 4,
    "credit": 224,
    "grade": 21
  },
  {
    "studentId": 54814,
    "schoolId": 899,
    "classId": 2429,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54822,
    "schoolId": 899,
    "classId": 2429,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54736,
    "schoolId": 899,
    "classId": 2428,
    "hp": 13,
    "credit": 39,
    "grade": 21
  },
  {
    "studentId": 54638,
    "schoolId": 899,
    "classId": 2425,
    "hp": 20,
    "credit": 146,
    "grade": 21
  },
  {
    "studentId": 54853,
    "schoolId": 899,
    "classId": 2430,
    "hp": 20,
    "credit": 62,
    "grade": 21
  },
  {
    "studentId": 54825,
    "schoolId": 899,
    "classId": 2430,
    "hp": 13,
    "credit": 29,
    "grade": 21
  },
  {
    "studentId": 54809,
    "schoolId": 899,
    "classId": 2429,
    "hp": 3,
    "credit": 7,
    "grade": 21
  },
  {
    "studentId": 54824,
    "schoolId": 899,
    "classId": 2430,
    "hp": 12,
    "credit": 51,
    "grade": 21
  },
  {
    "studentId": 54791,
    "schoolId": 899,
    "classId": 2429,
    "hp": 7,
    "credit": 52,
    "grade": 21
  },
  {
    "studentId": 54820,
    "schoolId": 899,
    "classId": 2429,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54819,
    "schoolId": 899,
    "classId": 2429,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54619,
    "schoolId": 899,
    "classId": 2425,
    "hp": 4,
    "credit": 78,
    "grade": 21
  },
  {
    "studentId": 54861,
    "schoolId": 899,
    "classId": 2430,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54603,
    "schoolId": 899,
    "classId": 2425,
    "hp": 14,
    "credit": 95,
    "grade": 21
  },
  {
    "studentId": 54600,
    "schoolId": 899,
    "classId": 2425,
    "hp": 8,
    "credit": 83,
    "grade": 21
  },
  {
    "studentId": 54793,
    "schoolId": 899,
    "classId": 2429,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54620,
    "schoolId": 899,
    "classId": 2425,
    "hp": 4,
    "credit": 118,
    "grade": 21
  },
  {
    "studentId": 54602,
    "schoolId": 899,
    "classId": 2425,
    "hp": 5,
    "credit": 164,
    "grade": 21
  },
  {
    "studentId": 54813,
    "schoolId": 899,
    "classId": 2429,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54660,
    "schoolId": 899,
    "classId": 2426,
    "hp": 0,
    "credit": 50,
    "grade": 21
  },
  {
    "studentId": 54864,
    "schoolId": 899,
    "classId": 2430,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54743,
    "schoolId": 899,
    "classId": 2428,
    "hp": 6,
    "credit": 76,
    "grade": 21
  },
  {
    "studentId": 54810,
    "schoolId": 899,
    "classId": 2429,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54653,
    "schoolId": 899,
    "classId": 2426,
    "hp": 9,
    "credit": 44,
    "grade": 21
  },
  {
    "studentId": 54821,
    "schoolId": 899,
    "classId": 2429,
    "hp": 5,
    "credit": 45,
    "grade": 21
  },
  {
    "studentId": 54844,
    "schoolId": 899,
    "classId": 2430,
    "hp": 11,
    "credit": 68,
    "grade": 21
  },
  {
    "studentId": 54783,
    "schoolId": 899,
    "classId": 2429,
    "hp": 20,
    "credit": 48,
    "grade": 21
  },
  {
    "studentId": 54805,
    "schoolId": 899,
    "classId": 2429,
    "hp": 10,
    "credit": 35,
    "grade": 21
  },
  {
    "studentId": 54740,
    "schoolId": 899,
    "classId": 2428,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54765,
    "schoolId": 899,
    "classId": 2428,
    "hp": 11,
    "credit": 33,
    "grade": 21
  },
  {
    "studentId": 54733,
    "schoolId": 899,
    "classId": 2428,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54802,
    "schoolId": 899,
    "classId": 2429,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54741,
    "schoolId": 899,
    "classId": 2428,
    "hp": 11,
    "credit": 199,
    "grade": 21
  },
  {
    "studentId": 54857,
    "schoolId": 899,
    "classId": 2430,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54768,
    "schoolId": 899,
    "classId": 2428,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54839,
    "schoolId": 899,
    "classId": 2430,
    "hp": 20,
    "credit": 65,
    "grade": 21
  },
  {
    "studentId": 54759,
    "schoolId": 899,
    "classId": 2428,
    "hp": 3,
    "credit": 35,
    "grade": 21
  },
  {
    "studentId": 54680,
    "schoolId": 899,
    "classId": 2426,
    "hp": 1,
    "credit": 54,
    "grade": 21
  },
  {
    "studentId": 54797,
    "schoolId": 899,
    "classId": 2429,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54799,
    "schoolId": 899,
    "classId": 2429,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54796,
    "schoolId": 899,
    "classId": 2429,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54737,
    "schoolId": 899,
    "classId": 2428,
    "hp": 14,
    "credit": 38,
    "grade": 21
  },
  {
    "studentId": 54683,
    "schoolId": 899,
    "classId": 2426,
    "hp": -2,
    "credit": 26,
    "grade": 21
  },
  {
    "studentId": 54649,
    "schoolId": 899,
    "classId": 2426,
    "hp": 10,
    "credit": 60,
    "grade": 21
  },
  {
    "studentId": 54670,
    "schoolId": 899,
    "classId": 2426,
    "hp": 10,
    "credit": 42,
    "grade": 21
  },
  {
    "studentId": 54787,
    "schoolId": 899,
    "classId": 2429,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54778,
    "schoolId": 899,
    "classId": 2429,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54685,
    "schoolId": 899,
    "classId": 2426,
    "hp": 20,
    "credit": 74,
    "grade": 21
  },
  {
    "studentId": 54832,
    "schoolId": 899,
    "classId": 2430,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54657,
    "schoolId": 899,
    "classId": 2426,
    "hp": 2,
    "credit": 52,
    "grade": 21
  },
  {
    "studentId": 54650,
    "schoolId": 899,
    "classId": 2426,
    "hp": 4,
    "credit": 43,
    "grade": 21
  },
  {
    "studentId": 54705,
    "schoolId": 899,
    "classId": 2427,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54722,
    "schoolId": 899,
    "classId": 2427,
    "hp": 12,
    "credit": 36,
    "grade": 21
  },
  {
    "studentId": 54698,
    "schoolId": 899,
    "classId": 2427,
    "hp": 10,
    "credit": 55,
    "grade": 21
  },
  {
    "studentId": 54838,
    "schoolId": 899,
    "classId": 2430,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54707,
    "schoolId": 899,
    "classId": 2427,
    "hp": 20,
    "credit": 135,
    "grade": 21
  },
  {
    "studentId": 54713,
    "schoolId": 899,
    "classId": 2427,
    "hp": 20,
    "credit": 405,
    "grade": 21
  },
  {
    "studentId": 54700,
    "schoolId": 899,
    "classId": 2427,
    "hp": 15,
    "credit": 90,
    "grade": 21
  },
  {
    "studentId": 54628,
    "schoolId": 899,
    "classId": 2425,
    "hp": 4,
    "credit": 31,
    "grade": 21
  },
  {
    "studentId": 54621,
    "schoolId": 899,
    "classId": 2425,
    "hp": 20,
    "credit": 57,
    "grade": 21
  },
  {
    "studentId": 54731,
    "schoolId": 899,
    "classId": 2427,
    "hp": 14,
    "credit": 37,
    "grade": 21
  },
  {
    "studentId": 54694,
    "schoolId": 899,
    "classId": 2427,
    "hp": -4,
    "credit": 31,
    "grade": 21
  },
  {
    "studentId": 54690,
    "schoolId": 899,
    "classId": 2427,
    "hp": 5,
    "credit": 32,
    "grade": 21
  },
  {
    "studentId": 54720,
    "schoolId": 899,
    "classId": 2427,
    "hp": 10,
    "credit": 46,
    "grade": 21
  },
  {
    "studentId": 54708,
    "schoolId": 899,
    "classId": 2427,
    "hp": 13,
    "credit": 39,
    "grade": 21
  },
  {
    "studentId": 54692,
    "schoolId": 899,
    "classId": 2427,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54843,
    "schoolId": 899,
    "classId": 2430,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54686,
    "schoolId": 899,
    "classId": 2426,
    "hp": 3,
    "credit": 95,
    "grade": 21
  },
  {
    "studentId": 54669,
    "schoolId": 899,
    "classId": 2426,
    "hp": 5,
    "credit": 76,
    "grade": 21
  },
  {
    "studentId": 54718,
    "schoolId": 899,
    "classId": 2427,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54632,
    "schoolId": 899,
    "classId": 2425,
    "hp": 1,
    "credit": 72,
    "grade": 21
  },
  {
    "studentId": 54636,
    "schoolId": 899,
    "classId": 2425,
    "hp": 7,
    "credit": 79,
    "grade": 21
  },
  {
    "studentId": 54693,
    "schoolId": 899,
    "classId": 2427,
    "hp": 6,
    "credit": 19,
    "grade": 21
  },
  {
    "studentId": 54866,
    "schoolId": 899,
    "classId": 2430,
    "hp": 8,
    "credit": 18,
    "grade": 21
  },
  {
    "studentId": 54842,
    "schoolId": 899,
    "classId": 2430,
    "hp": 12,
    "credit": 36,
    "grade": 21
  },
  {
    "studentId": 54682,
    "schoolId": 899,
    "classId": 2426,
    "hp": 8,
    "credit": 36,
    "grade": 21
  },
  {
    "studentId": 54766,
    "schoolId": 899,
    "classId": 2428,
    "hp": 7,
    "credit": 33,
    "grade": 21
  },
  {
    "studentId": 54865,
    "schoolId": 899,
    "classId": 2430,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54611,
    "schoolId": 899,
    "classId": 2425,
    "hp": -2,
    "credit": 135,
    "grade": 21
  },
  {
    "studentId": 54601,
    "schoolId": 899,
    "classId": 2425,
    "hp": 0,
    "credit": 138,
    "grade": 21
  },
  {
    "studentId": 54665,
    "schoolId": 899,
    "classId": 2426,
    "hp": 12,
    "credit": 147,
    "grade": 21
  },
  {
    "studentId": 54841,
    "schoolId": 899,
    "classId": 2430,
    "hp": 10,
    "credit": 35,
    "grade": 21
  },
  {
    "studentId": 54634,
    "schoolId": 899,
    "classId": 2425,
    "hp": 20,
    "credit": 49,
    "grade": 21
  },
  {
    "studentId": 54721,
    "schoolId": 899,
    "classId": 2427,
    "hp": 10,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54773,
    "schoolId": 899,
    "classId": 2428,
    "hp": 8,
    "credit": 26,
    "grade": 21
  },
  {
    "studentId": 54661,
    "schoolId": 899,
    "classId": 2426,
    "hp": 20,
    "credit": 60,
    "grade": 21
  },
  {
    "studentId": 54612,
    "schoolId": 899,
    "classId": 2425,
    "hp": 1,
    "credit": 75,
    "grade": 21
  },
  {
    "studentId": 54658,
    "schoolId": 899,
    "classId": 2426,
    "hp": 20,
    "credit": 47,
    "grade": 21
  },
  {
    "studentId": 54847,
    "schoolId": 899,
    "classId": 2430,
    "hp": 17,
    "credit": 33,
    "grade": 21
  },
  {
    "studentId": 54786,
    "schoolId": 899,
    "classId": 2429,
    "hp": 12,
    "credit": 35,
    "grade": 21
  },
  {
    "studentId": 54703,
    "schoolId": 899,
    "classId": 2427,
    "hp": 20,
    "credit": 39,
    "grade": 21
  },
  {
    "studentId": 54646,
    "schoolId": 899,
    "classId": 2426,
    "hp": 2,
    "credit": 41,
    "grade": 21
  },
  {
    "studentId": 54679,
    "schoolId": 899,
    "classId": 2426,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54633,
    "schoolId": 899,
    "classId": 2425,
    "hp": 11,
    "credit": 33,
    "grade": 21
  },
  {
    "studentId": 54618,
    "schoolId": 899,
    "classId": 2425,
    "hp": 20,
    "credit": 35,
    "grade": 21
  },
  {
    "studentId": 54662,
    "schoolId": 899,
    "classId": 2426,
    "hp": 4,
    "credit": 43,
    "grade": 21
  },
  {
    "studentId": 54668,
    "schoolId": 899,
    "classId": 2426,
    "hp": 17,
    "credit": 32,
    "grade": 21
  },
  {
    "studentId": 54855,
    "schoolId": 899,
    "classId": 2430,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54711,
    "schoolId": 899,
    "classId": 2427,
    "hp": 18,
    "credit": 41,
    "grade": 21
  },
  {
    "studentId": 54647,
    "schoolId": 899,
    "classId": 2426,
    "hp": 1,
    "credit": 45,
    "grade": 21
  },
  {
    "studentId": 54709,
    "schoolId": 899,
    "classId": 2427,
    "hp": 4,
    "credit": 29,
    "grade": 21
  },
  {
    "studentId": 54678,
    "schoolId": 899,
    "classId": 2426,
    "hp": 20,
    "credit": 134,
    "grade": 21
  },
  {
    "studentId": 54617,
    "schoolId": 899,
    "classId": 2425,
    "hp": 2,
    "credit": 41,
    "grade": 21
  },
  {
    "studentId": 54688,
    "schoolId": 899,
    "classId": 2427,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54624,
    "schoolId": 899,
    "classId": 2425,
    "hp": 17,
    "credit": 91,
    "grade": 21
  },
  {
    "studentId": 54750,
    "schoolId": 899,
    "classId": 2428,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54781,
    "schoolId": 899,
    "classId": 2429,
    "hp": 20,
    "credit": 140,
    "grade": 21
  },
  {
    "studentId": 54735,
    "schoolId": 899,
    "classId": 2428,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54725,
    "schoolId": 899,
    "classId": 2427,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54745,
    "schoolId": 899,
    "classId": 2428,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54677,
    "schoolId": 899,
    "classId": 2426,
    "hp": 6,
    "credit": 23,
    "grade": 21
  },
  {
    "studentId": 54640,
    "schoolId": 899,
    "classId": 2425,
    "hp": 13,
    "credit": 46,
    "grade": 21
  },
  {
    "studentId": 54631,
    "schoolId": 899,
    "classId": 2425,
    "hp": 14,
    "credit": 132,
    "grade": 21
  },
  {
    "studentId": 54803,
    "schoolId": 899,
    "classId": 2429,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54651,
    "schoolId": 899,
    "classId": 2426,
    "hp": 17,
    "credit": 27,
    "grade": 21
  },
  {
    "studentId": 54852,
    "schoolId": 899,
    "classId": 2430,
    "hp": 9,
    "credit": 38,
    "grade": 21
  },
  {
    "studentId": 54616,
    "schoolId": 899,
    "classId": 2425,
    "hp": -2,
    "credit": 67,
    "grade": 21
  },
  {
    "studentId": 54623,
    "schoolId": 899,
    "classId": 2425,
    "hp": 9,
    "credit": 175,
    "grade": 21
  },
  {
    "studentId": 54730,
    "schoolId": 899,
    "classId": 2427,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54723,
    "schoolId": 899,
    "classId": 2427,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54823,
    "schoolId": 899,
    "classId": 2430,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54615,
    "schoolId": 899,
    "classId": 2425,
    "hp": -1,
    "credit": 69,
    "grade": 21
  },
  {
    "studentId": 54599,
    "schoolId": 899,
    "classId": 2425,
    "hp": 11,
    "credit": 48,
    "grade": 21
  },
  {
    "studentId": 54775,
    "schoolId": 899,
    "classId": 2428,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54727,
    "schoolId": 899,
    "classId": 2427,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54674,
    "schoolId": 899,
    "classId": 2426,
    "hp": 15,
    "credit": 68,
    "grade": 21
  },
  {
    "studentId": 54850,
    "schoolId": 899,
    "classId": 2430,
    "hp": 7,
    "credit": 32,
    "grade": 21
  },
  {
    "studentId": 54614,
    "schoolId": 899,
    "classId": 2425,
    "hp": 18,
    "credit": 45,
    "grade": 21
  },
  {
    "studentId": 54656,
    "schoolId": 899,
    "classId": 2426,
    "hp": -2,
    "credit": 156,
    "grade": 21
  },
  {
    "studentId": 54760,
    "schoolId": 899,
    "classId": 2428,
    "hp": 15,
    "credit": 133,
    "grade": 21
  },
  {
    "studentId": 54706,
    "schoolId": 899,
    "classId": 2427,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54849,
    "schoolId": 899,
    "classId": 2430,
    "hp": 16,
    "credit": 23,
    "grade": 21
  },
  {
    "studentId": 54801,
    "schoolId": 899,
    "classId": 2429,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54715,
    "schoolId": 899,
    "classId": 2427,
    "hp": 8,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54607,
    "schoolId": 899,
    "classId": 2425,
    "hp": 6,
    "credit": 71,
    "grade": 21
  },
  {
    "studentId": 54676,
    "schoolId": 899,
    "classId": 2426,
    "hp": 18,
    "credit": 24,
    "grade": 21
  },
  {
    "studentId": 54845,
    "schoolId": 899,
    "classId": 2430,
    "hp": 19,
    "credit": 60,
    "grade": 21
  },
  {
    "studentId": 54777,
    "schoolId": 899,
    "classId": 2428,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54671,
    "schoolId": 899,
    "classId": 2426,
    "hp": 20,
    "credit": 90,
    "grade": 21
  },
  {
    "studentId": 54672,
    "schoolId": 899,
    "classId": 2426,
    "hp": 11,
    "credit": 45,
    "grade": 21
  },
  {
    "studentId": 54643,
    "schoolId": 899,
    "classId": 2426,
    "hp": 17,
    "credit": 42,
    "grade": 21
  },
  {
    "studentId": 54664,
    "schoolId": 899,
    "classId": 2426,
    "hp": -2,
    "credit": 73,
    "grade": 21
  },
  {
    "studentId": 54859,
    "schoolId": 899,
    "classId": 2430,
    "hp": 9,
    "credit": 179,
    "grade": 21
  },
  {
    "studentId": 69930,
    "schoolId": 899,
    "classId": 2430,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54663,
    "schoolId": 899,
    "classId": 2426,
    "hp": 17,
    "credit": 82,
    "grade": 21
  },
  {
    "studentId": 54728,
    "schoolId": 899,
    "classId": 2427,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54794,
    "schoolId": 899,
    "classId": 2429,
    "hp": 8,
    "credit": 59,
    "grade": 21
  },
  {
    "studentId": 54867,
    "schoolId": 899,
    "classId": 2430,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54642,
    "schoolId": 899,
    "classId": 2426,
    "hp": 15,
    "credit": 40,
    "grade": 21
  },
  {
    "studentId": 54648,
    "schoolId": 899,
    "classId": 2426,
    "hp": 13,
    "credit": 71,
    "grade": 21
  },
  {
    "studentId": 54645,
    "schoolId": 899,
    "classId": 2426,
    "hp": 1,
    "credit": 65,
    "grade": 21
  },
  {
    "studentId": 54655,
    "schoolId": 899,
    "classId": 2426,
    "hp": 0,
    "credit": 81,
    "grade": 21
  },
  {
    "studentId": 54625,
    "schoolId": 899,
    "classId": 2425,
    "hp": 20,
    "credit": 43,
    "grade": 21
  },
  {
    "studentId": 54639,
    "schoolId": 899,
    "classId": 2425,
    "hp": 20,
    "credit": 38,
    "grade": 21
  },
  {
    "studentId": 54827,
    "schoolId": 899,
    "classId": 2430,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54837,
    "schoolId": 899,
    "classId": 2430,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54742,
    "schoolId": 899,
    "classId": 2428,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54840,
    "schoolId": 899,
    "classId": 2430,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54704,
    "schoolId": 899,
    "classId": 2427,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54622,
    "schoolId": 899,
    "classId": 2425,
    "hp": 1,
    "credit": 135,
    "grade": 21
  },
  {
    "studentId": 54717,
    "schoolId": 899,
    "classId": 2427,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54792,
    "schoolId": 899,
    "classId": 2429,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54746,
    "schoolId": 899,
    "classId": 2428,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54812,
    "schoolId": 899,
    "classId": 2429,
    "hp": 15,
    "credit": -11,
    "grade": 21
  },
  {
    "studentId": 54860,
    "schoolId": 899,
    "classId": 2430,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54755,
    "schoolId": 899,
    "classId": 2428,
    "hp": 18,
    "credit": 14,
    "grade": 21
  },
  {
    "studentId": 54644,
    "schoolId": 899,
    "classId": 2426,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54652,
    "schoolId": 899,
    "classId": 2426,
    "hp": 13,
    "credit": 37,
    "grade": 21
  },
  {
    "studentId": 54666,
    "schoolId": 899,
    "classId": 2426,
    "hp": 13,
    "credit": 36,
    "grade": 21
  },
  {
    "studentId": 54684,
    "schoolId": 899,
    "classId": 2426,
    "hp": 19,
    "credit": 44,
    "grade": 21
  },
  {
    "studentId": 54654,
    "schoolId": 899,
    "classId": 2426,
    "hp": 11,
    "credit": 26,
    "grade": 21
  },
  {
    "studentId": 54667,
    "schoolId": 899,
    "classId": 2426,
    "hp": 1,
    "credit": 58,
    "grade": 21
  },
  {
    "studentId": 54681,
    "schoolId": 899,
    "classId": 2426,
    "hp": 9,
    "credit": 26,
    "grade": 21
  },
  {
    "studentId": 54675,
    "schoolId": 899,
    "classId": 2426,
    "hp": 7,
    "credit": 8,
    "grade": 21
  },
  {
    "studentId": 54673,
    "schoolId": 899,
    "classId": 2426,
    "hp": 3,
    "credit": 31,
    "grade": 21
  },
  {
    "studentId": 54714,
    "schoolId": 899,
    "classId": 2427,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54798,
    "schoolId": 899,
    "classId": 2429,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54695,
    "schoolId": 899,
    "classId": 2427,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54863,
    "schoolId": 899,
    "classId": 2430,
    "hp": 19,
    "credit": 37,
    "grade": 21
  },
  {
    "studentId": 54836,
    "schoolId": 899,
    "classId": 2430,
    "hp": 15,
    "credit": 36,
    "grade": 21
  },
  {
    "studentId": 54851,
    "schoolId": 899,
    "classId": 2430,
    "hp": 9,
    "credit": 33,
    "grade": 21
  },
  {
    "studentId": 54751,
    "schoolId": 899,
    "classId": 2428,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54764,
    "schoolId": 899,
    "classId": 2428,
    "hp": 3,
    "credit": 40,
    "grade": 21
  },
  {
    "studentId": 54862,
    "schoolId": 899,
    "classId": 2430,
    "hp": 16,
    "credit": 27,
    "grade": 21
  },
  {
    "studentId": 54776,
    "schoolId": 899,
    "classId": 2428,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54779,
    "schoolId": 899,
    "classId": 2429,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54856,
    "schoolId": 899,
    "classId": 2430,
    "hp": 20,
    "credit": 30,
    "grade": 21
  },
  {
    "studentId": 54784,
    "schoolId": 899,
    "classId": 2429,
    "hp": 13,
    "credit": 91,
    "grade": 21
  },
  {
    "studentId": 54710,
    "schoolId": 899,
    "classId": 2427,
    "hp": 2,
    "credit": 36,
    "grade": 21
  },
  {
    "studentId": 54780,
    "schoolId": 899,
    "classId": 2429,
    "hp": 20,
    "credit": 30,
    "grade": 21
  }
]
descnames = ['userid', 'username', 'schoolid', 'schoolname', 'classname', 'classid',
                     'bookname', 'bookid', 'hp', 'credit', 'countscore', 'numhomework', 'numselfwork',
                     'topicnum', 'countright', 'rightlv', 'counttime', 'datetime']
sqlsel1 = "select * from product_stw_daycount where schoolid in ('899') and bookid='5a2e4ac62c8afb18e6708fba'"
data_list  = session.execute(sqlsel1)
messes, mesind, finad = [], [], []
for datas in data_list:
    mess = {}
    for x in range(len(datas)):
        mess[descnames[x]] = datas[x]
    messes.append(mess)
for mes in messes:
    mesind.append(mes['userid'])
mesindex = list(set(mesind))
for y in mesindex:
    # findata=[]
    dataz = []
    for mes in messes:
        if mes['userid'] == y:
            dataz.append(mes)
    # findata.append(dataz)
    finad.append(dataz)
rdatafin=[]    
for dataf in finad:
    rdata={}
    num=[0,0,0,0,0,0]
    for z in range(len(dataf)):
        for i in range(len(dataf[z])):
            if i<=10:
                rdata[descnames[i]]=dataf[0][descnames[i]]
            elif i<=16:
                if dataf[z][descnames[i]]==None:
                    dataf[z][descnames[i]]=0
                num[i-11]+=dataf[z][descnames[i]]
                rdata[descnames[i]]=num[i-11]        
            else:
                if rdata[descnames[13]]==0:
                    rdata[descnames[15]]=rdata[descnames[16]]=0
                else:
                    rdata[descnames[15]]=int((rdata[descnames[14]]/rdata[descnames[13]])*1000)/10
                    rdata[descnames[16]]=int((rdata[descnames[16]]/rdata[descnames[13]])*10)/10
    rdatafin.append(rdata)

allmesses,mesind = [],[]
alldescs=['userid', 'username', 'schoolid', 'classname']
sqlsel = "select DISTINCT userid,username,schoolid,gradename from school_grade_user " \
                     "where gradename!='教师' AND schoolid in (%s)"% (schoolid)
data_lists = session.execute(sqlsel)
for datas in data_lists:
    mess = {}
    for x in range(len(alldescs)):
        mess[alldescs[x]] = datas[x]
    allmesses.append(mess)
    
findescnames=['countscore', 'numhomework', 'numselfwork','topicnum', 'countright', 'rightlv', 'counttime']
alldatas = []
for allmess in allmesses:
    for reqdata in reqdatas:
        for rdataf in rdatafin:
            if reqdata["studentId"] == int(allmess["userid"]):
                allmess["hp"] = reqdata["hp"]
                allmess["credit"] = reqdata["credit"]
            if rdataf["userid"] == int(allmess["userid"]):
                allmess["countscore"] = rdataf["countscore"]
                allmess["numhomework"] = rdataf["numhomework"]
                allmess["numselfwork"] = rdataf["numselfwork"]
                allmess["topicnum"] = rdataf["topicnum"]
                allmess["countright"] = rdataf["countright"]
                allmess["rightlv"] = rdataf["rightlv"]
                allmess["counttime"] = rdataf["counttime"]
    if len(allmess)==len(alldescs):
        allmess["credit"]=allmess["hp"]=0
    if len(allmess)==len(alldescs)+2:
        for findena in findescnames:
            allmess[findena]=0
    alldatas.append(allmess)
finall=[]
#for allmess in alldatas:
#    for reqdata in reqdatas:
#        for rdataf in rdatafin:
#            if reqdata["studentId"] == int(allmess["userid"]):
#                allmess["hp"] = reqdata["hp"]
#                allmess["credit"] = reqdata["credit"]
#    if len(allmess)==len(alldescs):
#        allmess["credit"]=allmess["hp"]=0
#    finall.append(allmess)
#finall=[]
#for allmes in alldatas:
#    for rdatafi in rdatafin:
#        for desnum in range(len(findescnames)):
#            if int(rdatafi["userid"]) == int(allmes["userid"]) and rdatafi["topicnum"]:
#                allmes[findescnames[desnum]]=rdatafi[findescnames[desnum]]
#            else:
#                allmes[findescnames[desnum]]=0
#    finall.append(allmes)
#for asd in finall:
#    if asd['userid']=='54677':
#        print(asd)
    
session.close()

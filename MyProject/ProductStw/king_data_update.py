# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 16:30:15 2018

@author: Administrator
"""

import pandas as pd
import pymongo
import time
import datetime
from datetime import timedelta
from flask import Flask
from flask_restplus import Api, Resource, fields, reqparse

app = Flask(__name__)
#app.config.SWAGGER_UI_OPERATION_ID = True
app.config.SWAGGER_UI_REQUEST_DURATION = True
api = Api(app, version='1.0', title='Bigdata',doc='/swagger-ui.html',
    description='Bigdata APIs',default_label=None,default=None, 
                   contact_email='lwc@quuedu.com', contact='Alex'
)

ns = api.namespace('刷题王测试数据', description='King Test Data',path='/api/v1')

def trans_time(time_stamp):
    time_stamp = int(time_stamp/1000)
    return time.strftime("%Y%m%d", time.localtime(time_stamp))

def data_df_xueqing():
    client = pymongo.MongoClient('192.168.5.52',50000)
    db  = client['king']
    pk10 = db['game']
    pk11 = db['student']
    game_data = pk10.find()
    projection_fields = {'_id': False, 'studentId': True, 'schoolId': True, 'className': True,
                                     'schoolId': True, 'classId': True, 'studentName': True}
    stu_data = pk11.find(projection=projection_fields )
    data = pd.DataFrame(list(game_data))
    data['qst_num']=data['questionList'].map(len)
    data['date_time']=data['createTime'].map(trans_time)
    stu = pd.DataFrame(list(stu_data))
    data = data.fillna(value=0)
    gp1 = data[(data['subjectId']==3) | (data['subjectId']==1)].groupby(
            ['studentId','date_time','subjectId'],as_index=False)
    gp2 = data[(data['subjectId']!=3) & (data['subjectId']!=1)].groupby(
            ['studentId','date_time','subjectId'],as_index=False)
    c1 = gp1['_id'].count()
    c1.rename(columns={'_id': 'qst_num'}, inplace = True) 
    #result =  pd.merge(c1,c2,on=['studentId','dateTime'])
    c3 = gp1['accuracy'].mean()
    c13 = pd.merge(c1,c3,on=['studentId','date_time','subjectId'])
    c13.rename(columns={'accuracy': 'right_rate'}, inplace = True)
    c2 = gp2['qst_num'].sum()
    c4 = gp2['questionRight'].sum()
    c24 = pd.merge(c2,c4,on=['studentId','date_time','subjectId'])
    c24['right_rate'] = c24['questionRight']/c24['qst_num']*100
    del (c24['questionRight'])
    #c4 = c2['questionRight']/c2['qstNum']
    result = c13.append(c24, ignore_index=True)
    result = pd.merge(result,stu,on=['studentId'])
    result['app_name'] = 'stw'
    result.rename(columns={'studentId':'user_id','classId':'class_id',
                           'className':'class_name','schoolId':'school_id',
                           'studentName':'user_name','subjectId':'subject_id'}, inplace = True)
    return result

def sql_insert(df,table_name,db_name,if_exists='replace'):
    from sqlalchemy import create_engine
    ##将数据写入mysql的数据库，但需要先通过sqlalchemy.create_engine建立连接,且字符编码设置为utf8，否则有些latin字符不能处理
    yconnect = create_engine('mysql+mysqldb://webmail_user:szw_webmail1234@192.168.5.53:3306/%s?charset=utf8'%db_name)
    pd.io.sql.to_sql(df,table_name, yconnect, index=False, 
                     schema=db_name, if_exists=if_exists)

def sql_select_student():
    from sqlalchemy import create_engine
    ##先通过sqlalchemy.create_engine建立连接,且字符编码设置为utf8，否则有些latin字符不能处理
    yconnect = create_engine('mysql+mysqldb://webmail_user:szw_webmail1234@192.168.5.53:3306/xh_webmanage?charset=utf8')
    sql1 = 'select a1.userId,a1.userName,a1.schoolId,a1.groupId, \
           a2.`name`,a2.clazzType from XHSchool_ClazzMembers a1\
        left join XHSchool_Clazzes a2 on a1.groupId=a2.id where departed=0'
    df1 = pd.io.sql.read_sql(sql1, yconnect)
    df1.rename(columns={'userId':'studentId','userName':'studentName',
                        'schoolId':'schoolId','groupId':'classId',
                        'name':'className','clazzType':'class_type'}, inplace=True)
    return df1
    

def clear_sql_table(table_name,db_name):
    from sqlalchemy import create_engine
    ##先通过sqlalchemy.create_engine建立连接,且字符编码设置为utf8，否则有些latin字符不能处理
    yconnect = create_engine('mysql+mysqldb://webmail_user:szw_webmail1234@192.168.5.53:3306/%s?charset=utf8'%db_name)
    sql1 = 'truncate table %s'%table_name
    try:
        pd.io.sql.read_sql(sql1, yconnect)
    except Exception as e:
        pass
    
    

def week_get(d):
    dayscount = datetime.timedelta(days=d.isoweekday())
    dayto = d - dayscount
    sixdays = datetime.timedelta(days=6*2)
    dayfrom = dayto - sixdays
    date_from = datetime.datetime(dayfrom.year, dayfrom.month, dayfrom.day, 0, 0, 0)
    date_to = datetime.datetime(dayto.year, dayto.month, dayto.day, 23, 59, 59)
    print ('---'.join([str(date_from), str(date_to)]))

    
def king_rank(st_date=19700101,en_date=29991231,is_weekly=1):  
    client = pymongo.MongoClient('192.168.5.52',50000)
    db  = client['king']
    pk10 = db['game']
    game_data = pk10.find()
    data = pd.DataFrame(list(game_data))
    data['qst_num'] = data['questionList'].map(len)
    data['date_time' ] = data['createTime'].map(trans_time).astype(int)
    #stu = pd.DataFrame(list(stu_data))
    stu = sql_select_student()
    data = data[(data['date_time']>=st_date) & (data['date_time']<=en_date)]
    data = data.fillna(value=0)
    gp1 = data[(data['subjectId']==3) | (data['subjectId']==1)].groupby(
            ['studentId','bookId','subjectId'],as_index=False)
    gp2 = data[(data['subjectId']!=3) & (data['subjectId']!=1)].groupby(
            ['studentId','bookId','subjectId'],as_index=False)
    c1 = gp1['_id'].count()
    c1.rename(columns={'_id': 'qst_num'}, inplace = True) 
    #result =  pd.merge(c1,c2,on=['studentId','dateTime'])
    c3 = gp1['accuracy'].mean()
    c13 = pd.merge(c1,c3,on=['studentId','bookId','subjectId'])
    c13['qst_right'] = 0
    c13.rename(columns={'accuracy': 'qst_right_rate'}, inplace=True)
    c2 = gp2['qst_num'].sum()
    c4 = gp2['questionRight'].sum()
    c24 = pd.merge(c2,c4,on=['studentId','bookId','subjectId'])
    c24['qst_right_rate'] = c24['questionRight']/c24['qst_num']*100
    c24.rename(columns={'questionRight':'qst_right'}, inplace=True)
    #del (c24['questionRight'])
    #c4 = c2['questionRight']/c2['qstNum']
    integral_data = data.groupby(['studentId','bookId'],as_index=False)['integral'].sum()
    integral_data['integral'] = integral_data['integral'].astype(int)
    word_data = data.groupby(['studentId','bookId'],as_index=False)['wordsMasterCount'].sum()
    word_data.rename(columns={'wordsMasterCount':'word_count'}, inplace=True)
    wi_data = pd.merge(integral_data,word_data, on=['studentId','bookId'])
    #a=data[(data['subjectId']==3) | (data['subjectId']==1)]
    result = c13.append(c24, ignore_index=True)
    result = pd.merge(result,wi_data, on=['studentId','bookId'])
    result = pd.merge(result,stu,on=['studentId'])
    result = result.round({'qst_right_rate':2})
    result.rename(columns={'studentId':'student_id','classId':'class_id','bookId':'book_id',
                           'className':'class_name','schoolId':'school_id','qst_num':'qst_count',
                           'studentName':'student_name','subjectId':'subject_id'
                           ,'integral':'intgral'}, inplace = True)
    result['is_weekly'] = is_weekly
    result['date_time'] = datetime.datetime.now().strftime('%Y%m%d')
    #cols=['school_id','book_id','subject_id']
    #result = result.ix[:,cols]
    return result
    
def king_rank_to_do():
    histrory_data = king_rank(is_weekly=1)
    now = datetime.datetime.now()
    bf_last_week_start = (now - timedelta(days=now.weekday()+14)).strftime('%Y%m%d')
    bf_last_week_end = (now - timedelta(days=now.weekday()+8)).strftime('%Y%m%d')
    bf_data = king_rank(int(bf_last_week_start),int(bf_last_week_end),4)
    
    last_week_start = (now - timedelta(days=now.weekday()+7)).strftime('%Y%m%d')
    last_week_end = (now - timedelta(days=now.weekday()+1)).strftime('%Y%m%d')
    last_data = king_rank(int(last_week_start),int(last_week_end),2)
    
    this_week_start = (now - timedelta(days=now.weekday())).strftime('%Y%m%d')
    this_week_end = (now + timedelta(days=6-now.weekday())).strftime('%Y%m%d')
    this_data = king_rank(int(this_week_start),int(this_week_end),3)
    
    result = ((histrory_data.append(bf_data, ignore_index=True)
            ).append(last_data, ignore_index=True)
            ).append(this_data, ignore_index=True)
    result.insert(0, 'id', result.index+1)
    cols=['id','school_id','book_id','subject_id','class_id','class_name',
          'class_type','student_id','student_name','intgral','word_count',
          'qst_count','qst_right','qst_right_rate','is_weekly','date_time']
    result = result.ix[:,cols]
    table_name = 'king_rank_daily_auto'
    db_name = 'xh_xueqing_test'
    clear_sql_table(table_name,db_name)
    sql_insert(result,table_name,db_name,'append')    
    
    
@ns.route('/getUpdate/xueqing')
class KingXueqing(Resource):
    '''学情测试数据接口'''
    key_words = api.parser()
    key_words.add_argument('password', required=True, type=str, help='密码', location='query')
    @ns.expect(key_words)
    def get(self):
        '''学情测试数据更新'''
        parser = reqparse.RequestParser()
        parser.add_argument('password', type=str)
        args = parser.parse_args()
        password = args.get('password','')
        if password == 'bigdata123':
            sta_time = time.time()
            result = data_df_xueqing()
            sql_insert(result,'product_qst_count','elasticsearch')
            end_time = time.time()
            time_cost = end_time - sta_time
            return 'Update Successful! Time cost %s(s)'%time_cost,200
        else:
            return 'Password was wrong!',400
            
@ns.route('/getUpdate/rank')
class KingRank(Resource):
    '''排行榜测试数据接口'''
    key_words = api.parser()
    key_words.add_argument('password', required=True, type=str, help='密码', location='query')
    @ns.expect(key_words)
    def get(self):
        '''排行榜测试数据更新'''
        parser = reqparse.RequestParser()
        parser.add_argument('password', type=str)
        args = parser.parse_args()
        password = args.get('password','')
        if password == 'bigdata123':
            sta_time = time.time()
            king_rank_to_do()
            end_time = time.time()
            time_cost = end_time - sta_time
            return 'Update Successful! Time cost %s(s)'%time_cost,200
        else:
            return 'Password was wrong!',400

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False,port=15001)
    

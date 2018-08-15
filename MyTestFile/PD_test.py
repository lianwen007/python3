# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 09:58:22 2018

@author: Administrator
"""
import time
import pandas as pd
from sqlalchemy import create_engine

class mysql_engine():
    user = 'webmail_user'
    passwd = 'szw_webmail1234'
    host = '192.168.5.53'
    port = '3306'
    db_name = 'xh_xueqing'
    engine = create_engine('mysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'.format(user,passwd,host,port,db_name))

def get_data(sql):
    pg_enine=mysql_engine()
    try:
        with pg_enine.engine.connect() as con, con.begin():
            df=pd.read_sql(sql,con)# 获取数据
            #df=pd.read_sql_table(sql,con)
        con.close()
    except:
        df=None
    return df

sql = 'select * from king_common_count_daily where school_id=4659'
sta1 = time.time()

#results = get_data(sql)
ora_engine=create_engine('mysql://webmail_user:szw_webmail1234@192.168.5.53:3306/xh_xueqing?charset=utf8')
conn=ora_engine.connect()
query_res=conn.execute(sql)
results=pd.DataFrame(columns=query_res.keys(),data=query_res.fetchall())

end1 = time.time()
print(end1-sta1)

sta = time.time()
#results = results.fillna(value=0)
sum_data = results.groupby(['student_id','book_id','subject_id'],as_index=False)['topic_num','game_integral'].sum()
avg_data = results[results['subject_id']!=3].groupby(['student_id','book_id','subject_id'],as_index=False)['qst_right_rate'].mean()
sum_3_data = results[results['subject_id']==3].groupby(['student_id','book_id','subject_id'],as_index=False)['topic_num'].sum()
avg_3_data = results[results['subject_id']==3].groupby(['student_id','book_id','subject_id'],as_index=False)['qst_right_rate'].mean()
avg_3d = pd.merge(sum_3_data,avg_3_data,on=['student_id','book_id','subject_id'])
avg_temp = avg_3d['qst_right_rate'].div(avg_3d['topic_num'])
avg_3d.insert(3, 'right_rate', avg_temp)
avg_3d.drop(['qst_right_rate','topic_num'],axis=1,inplace=True)
avg_3d.rename(columns={'right_rate':'qst_right_rate'}, inplace = True)
all_avg = avg_data.append(avg_3d, ignore_index=True)
#result =  sum_data.join(avg_data,how='outer',on=['studentId','bookId'])
result_gb =  pd.merge(sum_data,all_avg,on=['student_id','book_id','subject_id'])
end = time.time()
print(end-sta)

#筛选A列名字里面包括刘，且B列年龄大于60的，则更新数据D列的内容为1。不符合条件的行，D列数据不变
import pandas as pd

tdata = [
    {
      "classId": "4630", 
      "className": "\u9ad8\u4e0022\u73ed", 
      "practiceNum": 25, 
      "stuNum": "53", 
      "taskFixNum": 0, 
      "taskStuNum": 0, 
      "taskUploadNum": 0, 
      "tchId": 70152, 
      "tchName": "\u6731\u5747\u4f1f"
    }, 
    {
      "classId": "4631", 
      "className": "\u9ad8\u4e0023\u73ed", 
      "practiceNum": 2, 
      "stuNum": "55", 
      "taskFixNum": 0, 
      "taskStuNum": 0, 
      "taskUploadNum": 0, 
      "tchId": 70152, 
      "tchName": "\u6731\u5747\u4f1f"
    }, 
    {
      "classId": "4632", 
      "className": "\u9ad8\u4e0024\u73ed", 
      "practiceNum": 39, 
      "stuNum": "55", 
      "taskFixNum": 0, 
      "taskStuNum": 0, 
      "taskUploadNum": 0, 
      "tchId": 70152, 
      "tchName": "\u6731\u5747\u4f1f"
    }, 
    {
      "classId": "4633", 
      "className": "\u9ad8\u4e0025\u73ed", 
      "practiceNum": 2, 
      "stuNum": "51", 
      "taskFixNum": 0, 
      "taskStuNum": 0, 
      "taskUploadNum": 0, 
      "tchId": 70152, 
      "tchName": "\u6731\u5747\u4f1f"
    }, 
    {
      "classId": "4631", 
      "className": "\u9ad8\u4e0023\u73ed", 
      "practiceNum": 2, 
      "stuNum": "55", 
      "taskFixNum": 12, 
      "taskStuNum": 600, 
      "taskUploadNum": 50, 
      "tchId": 70155, 
      "tchName": "\u65bd\u7231\u840d"
    }, 
    {
      "classId": "4633", 
      "className": "\u9ad8\u4e0025\u73ed", 
      "practiceNum": 2, 
      "stuNum": "51", 
      "taskFixNum": 12, 
      "taskStuNum": 588, 
      "taskUploadNum": 50, 
      "tchId": 70155, 
      "tchName": "\u65bd\u7231\u840d"
    }
  ]
trs = pd.DataFrame(tdata)

dict_country = trs.to_json(orient='records')

rs = pd.DataFrame({'A':['我b45D','刘245D','刘123','刘123'],
                  'B':[20,30,60,80],
                    'D':[0,3,5,2]})
rs['D'][(rs['A'].str.contains('刘')) & (rs['B']>=60)] = 1



#import pandas as pd
#import pymysql
#import sys
#from sqlalchemy import create_engine
# 
#def read_mysql_and_insert():
#    
#    try:
#        conn = pymysql.connect(host='localhost',user='user1',password='123456',db='test',charset='utf8')
#    except pymysql.err.OperationalError as e:
#        print('Error is '+str(e))
#        sys.exit()
#        
#    try:
#        engine = create_engine('mysql+pymysql://user1:123456@localhost:3306/test')
#    except sqlalchemy.exc.OperationalError as e:
#        print('Error is '+str(e))
#        sys.exit()
#    except sqlalchemy.exc.InternalError as e:
#        print('Error is '+str(e))
#        sys.exit()
#        
#    try:   
#        sql = 'select * from sum_case'
#        df = pd.read_sql(sql, con=conn) 
#    except pymysql.err.ProgrammingError as e:
#        print('Error is '+str(e))
#        sys.exit() 
# 
#    print(df.head())
#    df.to_sql(name='sum_case_1',con=engine,if_exists='append',index=False)
#    conn.close()
#    print('ok')
#    
#if __name__ == '__main__':    
#    df = read_mysql_and_insert()

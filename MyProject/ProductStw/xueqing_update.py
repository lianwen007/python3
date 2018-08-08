import pandas as pd
import pymongo
import time
from flask import Flask
from flask_restplus import Api, Resource, fields, reqparse

app = Flask(__name__)
app.config.SWAGGER_UI_OPERATION_ID = True
app.config.SWAGGER_UI_REQUEST_DURATION = True
api = Api(app, version='1.0', title='Bigdata',doc='/swagger-ui.html',
    description='Bigdata APIs',default_label=None,default=None, 
                   contact_email='lwc@quuedu.com', contact='Alex'
)

ns = api.namespace('学情数据', description='king Info',path='/api/v1')

def trans_time(time_stamp):
    time_stamp = int(time_stamp/1000)
    return time.strftime("%Y%m%d", time.localtime(time_stamp))

def data_df():
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

def sql_insert(df):
    from sqlalchemy import create_engine
    ##将数据写入mysql的数据库，但需要先通过sqlalchemy.create_engine建立连接,且字符编码设置为utf8，否则有些latin字符不能处理
    yconnect = create_engine('mysql+mysqldb://webmail_user:szw_webmail1234@192.168.5.53:3306/elasticsearch?charset=utf8')
    pd.io.sql.to_sql(df,'product_qst_count', yconnect, index=False, 
                     schema='elasticsearch', if_exists='replace')

@ns.route('/getUpdate')
@ns.param('password', '密码')
class Todo(Resource):
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
            result = data_df()
            sql_insert(result)
            end_time = time.time()
            time_cost = end_time - sta_time
            return 'Update Successful! Time cost %s(s)'%time_cost,200
        else:
            return 'Password was wrong!',400


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=15001)

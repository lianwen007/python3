# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import pymongo
import time
import datetime
import random
import string
from datetime import timedelta
from flask import Flask
from sqlalchemy import create_engine
from flask_restplus import Api, Resource, fields, reqparse
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
# app.config.SWAGGER_UI_OPERATION_ID = True
app.config.SWAGGER_UI_REQUEST_DURATION = True
api = Api(app, version='1.0', title='Bigdata', doc='/swagger-ui.html',
          description='Bigdata APIs', default_label='', default='',
          contact_email='lwc@quuedu.com', contact='Alex'
          )
api.namespaces.clear()

ns = api.namespace('数据构造', description='Build Data', path='/api/v1')


class DataInsertBase(object):
    # 数据构造
    def __init__(self, *args, **kwargs):
        self.con_list = args
        self.con_dict = kwargs
        self.db_type = int(kwargs.get('db_type', 1))
        self.conn = None
        self.max_work = kwargs.get('max_work', 5)
        self.root_path = 'D:'

        # 数据库连接参数
        self.db_user = kwargs.get('db_user', 'root')
        self.db_password = kwargs.get('db_password', 'root')
        self.db_host = kwargs.get('db_host', 'localhost')
        self.db_port = kwargs.get('db_port', 3306)
        self.db_name = kwargs.get('db_name', 'test')
        self.table_name = kwargs.get('table_name', None)
        self.find_tables_sql = ''
        self.if_exists = kwargs.get('if_exists', 'append')

        # 数据构造参数
        self.start_time = kwargs.get('start_time', 946656000)
        self.end_time = kwargs.get('end_time', 1537800000)
        self.line_num = kwargs.get('line_num', 10)
        self.int_size = kwargs.get('int_size', 1)
        self.float_start = kwargs.get('float_start', 0)
        self.float_end = kwargs.get('float_end', 10)
        self.str_size = kwargs.get('str_size', 2)
        self.str_size_cn = kwargs.get('str_size_cn', 3)

    def db_connect(self):
        if self.db_type < 4:
            if self.db_type == 1:  # Mysql
                self.conn = 'mysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'
                self.find_tables_sql = "select table_name from information_schema.tables " \
                                       "where table_type='BASE TABLE' and table_schema='{0}'"
            elif self.db_type == 2:  # Oracle
                self.conn = 'oracle://{0}:{1}@{2}:{3}/{4}'
                self.find_tables_sql = ""
            elif self.db_type == 3:  # PG
                self.conn = 'postgresql://{0}:{1}@{2}:{3}/{4}'
                self.find_tables_sql = "SELECT tablename as table_name FROM pg_tables WHERE SCHEMANAME = '{0}'"
            conn_url = self.conn.format(self.db_user, self.db_password, self.db_host, self.db_port, self.db_name)
            return create_engine(conn_url)
        if self.db_type == 4:  # MongoDB
            client = pymongo.MongoClient(self.db_host, self.db_port)
            self.find_tables_sql = ''
            mongo_db = client[self.db_name]
            return mongo_db

    def get_all_tables(self):
        if self.table_name:
            tab_list = self.table_name.split(',')
        else:
            try:
                if self.db_type == 3:
                    df = pd.io.sql.read_sql(self.find_tables_sql.format('public'), self.db_connect())
                else:
                    df = pd.io.sql.read_sql(self.find_tables_sql.format(self.db_name), self.db_connect())
                tab_list = df['table_name'].tolist()
            except Exception as e:
                raise e
        return tab_list

    def data_build(self, db_table):
        if self.db_type < 4:
            df = pd.io.sql.read_sql(db_table, self.db_connect())
        else:
            db_find = self.db_connect()
            df = pd.DataFrame(db_find[db_table].find())
        df_column = df.columns.tolist()
        for x in df_column:
            if pd.api.types.is_string_dtype(df[x]):
                if 'name' in x:
                    df[x] = self.build_str_cn()
                elif 'addr' in x:
                    self.str_size_cn = 10
                    df[x] = self.build_str_cn()
                elif 'type' in x:
                    df[x] = random.choice(['a', 'b', 'c', 'd'])
                else:
                    df[x] = self.build_str()
            elif pd.api.types.is_integer_dtype(df[x]):
                df[x] = self.build_int()
            elif pd.api.types.is_float_dtype(df[x]):
                df[x] = self.build_float()
            elif pd.api.types.is_datetime64_any_dtype(df[x]):
                df[x] = self.build_time()
            else:
                df[x] = self.build_str()
        print(df)
        try:
            if self.db_type == 3:
                schema_name = 'public'
            else:
                schema_name = self.table_name
            pd.io.sql.to_sql(df, db_table, self.db_connect(), index=False,
                             schema=schema_name, if_exists=self.if_exists)
        except Exception as e:
            raise e
        return df.to_dict(orient='records')  # True

    def build_time(self):
        # 时间类型
        def time_exchange(x):
            result = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(x))
            return result

        data_time = pd.DataFrame(np.random.randint(self.start_time, self.end_time, size=self.line_num),
                                 columns=['datetime'])
        data_time['datetime'] = data_time['datetime'].map(time_exchange)
        return data_time

    def build_int(self):
        # 整数类型
        data_num = np.random.randint(10 ** (self.int_size - 1), 10 ** self.int_size, size=self.line_num)
        data_num = pd.DataFrame(data_num, columns=['int_data'])
        return data_num

    def build_float(self):
        # 浮点数
        data_num = np.random.uniform(self.float_start, self.float_end, size=self.line_num)
        data_num = pd.DataFrame(data_num, columns=['float_data'])
        return data_num

    def build_str(self):
        # 英文加数字
        str_list = list()
        for i in range(self.line_num):
            ran_str = ''.join(random.sample(string.ascii_letters + string.digits, self.str_size))
            str_list.append(ran_str)
        result = pd.DataFrame(str_list, columns=['str_data'])
        return result

    def build_str_cn(self):
        # 中文字符
        if self.str_size_cn == 3:
            cn_size = random.choice([2, 3])
        else:
            cn_size = self.str_size_cn
        str_list = list()
        for i in range(self.line_num):
            build_str = ''
            for x in range(cn_size):
                head = random.randint(0xb0, 0xf7)
                body = random.randint(0xa1, 0xf9)  # 在head区号为55的那一块最后5个汉字是乱码,为了方便缩减下范围
                val = f'{head:x}{body:x}'
                ran_str = bytes.fromhex(val).decode('gb2312')
                build_str = build_str + ran_str
            str_list.append(build_str)
        result = pd.DataFrame(str_list, columns=['str_cn'])
        return result

    def set_log(self, *args, **kwargs):
        # time.time() 返回 unix time
        # 如何把 unix time 转换为普通人类可以看懂的格式呢？
        fmt = '%Y/%m/%d %H:%M:%S'
        value = time.localtime(int(time.time()))
        log_dt = time.strftime(fmt, value)
        dt = time.strftime('%Y%m%d', time.localtime(int(time.time())))
        # 这样确保了每次运行都有一个独立的 path 存放 log
        path = self.root_path + 'etl.log.{}.txt'.format(dt)
        with open(path, 'a', encoding='utf-8') as f:
            print(log_dt, *args, file=f, **kwargs)

    def main(self):
        with ThreadPoolExecutor(max_workers=self.max_work) as executor:
            for x in self.get_all_tables():
                future_task = executor.submit(self.data_build, x)
                if future_task.running():
                    # self.set_log
                    print('%s is running' % str(future_task))
        return True


@ns.route('/dataBuild/insert')
class DataBuild(Resource):
    ''' 数据构造接口 '''
    key_words = api.parser()
    key_words.add_argument('db_type', required=True, type=int, help='数据库类型（1:MySql|2:oracle|3:pgsql|4:mongodb）', location='query')
    key_words.add_argument('db_host', required=True, type=str, help='主机地址', location='query')
    key_words.add_argument('db_port', required=True, type=int, help='端口号', location='query')
    key_words.add_argument('db_name', required=False, type=str, help='库名', location='query')
    key_words.add_argument('db_user', required=False, type=str, help='用户', location='query')
    key_words.add_argument('db_password', required=False, type=str, help='密码', location='query')
    key_words.add_argument('table_name', required=False, type=str, help='表名（逗号分隔，留空为所有表）', location='query')
    key_words.add_argument('line_num', required=False, type=int, help='插入条数', location='query')
    key_words.add_argument('if_exists', required=False, type=str, help='插入模式（\'append\':追加|\'replace\':覆盖）', location='query')
    key_words.add_argument('max_work', required=False, type=int, help='线程数', location='query')

    @ns.expect(key_words)
    def post(self):
        '''构造数据接口'''
        parser = reqparse.RequestParser()
        parser.add_argument('db_type', type=int)
        parser.add_argument('db_host', type=str)
        parser.add_argument('db_port', type=int)
        parser.add_argument('db_name', type=str)
        parser.add_argument('db_user', type=str)
        parser.add_argument('db_password', type=str)
        parser.add_argument('table_name', type=str)
        parser.add_argument('line_num', type=int)
        parser.add_argument('if_exists', type=str)
        parser.add_argument('max_work', type=int)
        values = parser.parse_args()
        print(values)
        # a = values.get('db_type')

        run_fun = DataInsertBase(**values)
        sta_time = time.time()
        result = run_fun.main()

        end_time = time.time()
        time_cost = end_time - sta_time
        print(result)
        if result:
            return 'Data Build Successful! Time cost %s(s)' % time_cost, 200
        else:
            return 'Error', 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)

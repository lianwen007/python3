import pymongo
import pymysql
import time
from config import mongo_url, etl_log_path, mysql_config


def mongo_client():
    # Mongo连接
    client = pymongo.MongoClient(mongo_url)
    return client.xh_king


def mysql_client(dbname):
    # Mysql 连接函数，参数为库名
    m = mysql_config
    db_client = pymysql.connect(host=m.get('hostname'), port=m.get('port'), user=m.get('user'),
                                passwd=m.get('password'), db=dbname, charset='utf8',)
    return db_client


def set_time_path():
    fmt = '%Y%m%d'  # %H%M%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(fmt, value)
    return dt


def set_log(*args, **kwargs):
    # time.time() 返回 unix time
    # 如何把 unix time 转换为普通人类可以看懂的格式呢？
    fmt = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    log_dt = time.strftime(fmt, value)
    dt = set_time_path()
    # 这样确保了每次运行都有一个独立的 path 存放 log
    path = etl_log_path + '/etl.log.{}.txt'.format(dt)
    with open(path, 'a', encoding='utf-8') as f:
        print(log_dt, *args, file=f, **kwargs)


def create_dirs(file_path):
    import os
    if not os.path.exists(file_path):  # 判断文件是否存在，返回布尔值
        os.makedirs(file_path)

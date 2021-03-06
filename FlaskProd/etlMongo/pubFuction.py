import pymongo
import time
from config import mongo_url, etl_log_path


def mongo_client():
    # Mongo连接
    client = pymongo.MongoClient(mongo_url)
    return client.xh_king


def set_time_path():
    fmt = '%Y%m%d'# %H%M%S'
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

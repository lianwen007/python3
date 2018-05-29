from config import mongo_url
from concurrent.futures import ThreadPoolExecutor
from .pubFunction import set_log as log
import pymongo
import time


class MongoEtlThread(object):
    def __init__(self, *args, **kwargs):
        self.mongo_uri = kwargs.get('mongo_url', mongo_url)
        self.collection_name = kwargs.get('collection_name', '')
        self.table_name = kwargs.get('table_name', '')
        self.values_get = kwargs.get('values_get', tuple())
        self.limit_num = kwargs.get('limit_num', 10000)
        self.max_works = kwargs.get('max_works', 5)
        self.root_path = kwargs.get('export_path', '')

    def get_result_num(self):
        try:
            result_num = getattr(getattr(pymongo.MongoClient(
                self.mongo_uri), self.collection_name), self.table_name).count()
        except Exception as e:
            set_log(e)
        return result_num

    def set_time_path(self):
        fmt = '%Y%m%d'  # %H%M%S'
        value = time.localtime(int(time.time()))
        dt = time.strftime(fmt, value)
        return dt

    def set_log(self, *args, **kwargs):
        # time.time() 返回 unix time
        # 如何把 unix time 转换为普通人类可以看懂的格式呢？
        fmt = '%Y/%m/%d %H:%M:%S'
        value = time.localtime(int(time.time()))
        log_dt = time.strftime(fmt, value)
        dt = self.set_time_path()
        # 这样确保了每次运行都有一个独立的 path 存放 log
        path = self.root_path + '/etl.log.{}.txt'.format(dt)
        with open(path, 'a', encoding='utf-8') as f:
            print(log_dt, *args, file=f, **kwargs)

    def mongo_to_txt(self, export_path, skip_num=0):
        sta = time.time()
        with open(export_path, 'a', encoding='utf-8') as f:
            # for i in range(int(result_num/limit_num)+1):  # 总条数对应限定查询条数做循环
            all_mess = ''  # 每次循环对要插入的数据字段做初始化
            results = getattr(getattr(pymongo.MongoClient(self.mongo_uri),
                                      self.collection_name), self.table_name). \
                find(skip=skip_num, limit=self.limit_num)  # 通过SKIP和LIMIT参数,对查询做限定条件
            for result in results:
                values = list()
                if self.values_get:
                    for v_get in self.values_get:
                        values.append(str(result.get(v_get, 0)))
                else:
                    for data in result.values():
                        values.append(str(data))
                messes = '\t'.join(values) + '\n'
                all_mess += messes
            f.write(all_mess)  # 等待本次结果集循环结束，一次性插入限定条数的数据
        end = time.time()
        log('time[{}]:{}'.format(skip_num, end - sta))
        return 1

    def thread_deal(self):
        dt = self.set_time_path()
        result_num = self.get_result_num()
        log("Table '{}' counts: {}".format(self.table_name, result_num))
        circle_max = int(result_num / (self.limit_num * self.max_works)) + 1
        # 循环的最大次数
        with ThreadPoolExecutor(max_workers=self.max_works) as executor:
            circle_num = 0  # 循环初始化
            while circle_num < circle_max:
                for i in range(self.max_works):
                    path_name = '{0}{1}_{2}_{3}.txt'.format(self.root_path, self.table_name, dt, i+1)
                    # 各个进程分配到不同的路径
                    skip_num = self.limit_num * (circle_num * self.max_works + i)  # 跳过数：需确保数据不缺失
                    if result_num >= skip_num:
                        future_task = executor.submit(self.mongo_to_txt, path_name, skip_num)
                    else:
                        break
                    if future_task.running():
                        log('%s is running' % str(future_task))
                circle_num += 1
        return 1

      

def mongo_etl(mongo_uri='', collections='', table_name='',
              path_name='', values_get=tuple(), limit_num=10000,
              thread_num=1):
    i = 0
    result_num = getattr(getattr(pymongo.MongoClient(mongo_uri), collections), table_name).count()
    while i < int(result_num/limit_num)+1:
        local_name = path_name + table_name + '_' + str(i+1) + '.txt'
        with open(local_name, 'a', encoding='utf-8') as f:
            # for i in range(int(result_num/limit_num)+1):  # 总条数对应限定查询条数做循环
            all_mess = ''  # 每次循环对要插入的数据字段做初始化
            results = getattr(getattr(pymongo.MongoClient(mongo_uri), collections), table_name).\
                find(skip=i*limit_num, limit=limit_num)
            # 对查询做限定条件，通过SKIP和LIMIT参数
            # print(result_num)  # 打印总条数
            # print(i+1)  # 打印共循环了几次
            for result in results:
                values = list()
                if values_get:
                    for v_get in values_get:
                        values.append(str(result.get(v_get, 0)))
                else:
                    for data in result.values():
                        values.append(str(data))
                messes = '\t'.join(values) + '\n'
                all_mess += messes
            f.write(all_mess)  # 等待本次结果集循环结束，一次性插入限定条数的数据
            i += 1


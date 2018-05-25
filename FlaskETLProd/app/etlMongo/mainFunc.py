from config import mongo_url
import pymongo


def mongo_etl(mongo_uri='', collections='', table_name='', path_name='', values_get=tuple(), limit_num=10000, ):
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
                for v_get in values_get:
                    values.append(str(result.get(v_get, 0)))
                messes = '\t'.join(values) + '\n'
                all_mess += messes
            f.write(all_mess)  # 等待本次结果集循环结束，一次性插入限定条数的数据
            i += 1

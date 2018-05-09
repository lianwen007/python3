limit_num = 100  # 指定每次查询的数据条数

mongo_url = "192.168.5.52:50000"
client = pymongo.MongoClient(mongo_url)
result_num = client.king.game.count()  # 获取mongo表中的总条数

fileObject = open('e:\\test0509.txt', 'a')
udatetime = int(time.time())
print(result_num)
# for 循环方法
for i in range(int(result_num/limit_num)+1):  # 总条数对应限定查询条数做循环
    all_mess = ''  # 每次循环对要插入的数据字段做初始化
    results = client.king.game.find(skip=(i)*limit_num,limit=limit_num)
    # 对查询做限定条件，通过SKIP和LIMIT参数
    # print(i)  # 打印共循环了几次
    for result in results:
        values = list()
        values.append(str(result['_id']))  # 局ID
        values.append(str(result['studentId']))  # 学生ID
        values.append(str(result['bookId']))  # 书ID
        values.append(str(result['createTime']))  # 创建时间
        values.append(str(result['updateTime']))  # 更新时间
        messes = '\t'.join(values) + '\n'
        all_mess += messes
    fileObject.write(all_mess)  # 等待本次结果集循环结束，一次性插入限定条数的数据
fileObject.close()



# while 方法
i = 0
while i < int(result_num/limit_num)+1:
#for i in range(int(result_num/limit_num)+1):  # 总条数对应限定查询条数做循环
    all_mess = ''  # 每次循环对要插入的数据字段做初始化
    results = client.king.game.find(skip=(i)*limit_num,limit=limit_num)
    # 对查询做限定条件，通过SKIP和LIMIT参数
    print(i+1)  # 打印共循环了几次
    for result in results:
        values = list()
        values.append(str(result['_id']))  # 局ID
        values.append(str(result['studentId']))  # 学生ID
        values.append(str(result['bookId']))  # 书ID
        values.append(str(result['createTime']))  # 创建时间
        values.append(str(result['updateTime']))  # 更新时间
        messes = '\t'.join(values) + '\n'
        all_mess += messes
    fileObject.write(all_mess)  # 等待本次结果集循环结束，一次性插入限定条数的数据
    i +=1
fileObject.close()


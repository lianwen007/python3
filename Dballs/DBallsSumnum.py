import random
import pymysql
from random import randint
from collections import defaultdict
     
class DieBlue():
    def __init__(self,num_sides=15):
        self.num_sides=num_sides        
    def roll(self):
        return randint(1,self.num_sides)

def diered(ballnumbers=33):
    ballnumb=ballnumbers
    return random.sample(range(1,ballnumb),6)

sumnum=[]

#计算1万次随机
for k in range(10000):
    resultssum=0
    dieblue=DieBlue()
    results=[]
    resultred=[]
    for resultred in diered():
        results.append(resultred)
    resultblue=dieblue.roll() 
    results.append(resultblue)
    for i in range(7):
        resultssum += results[i]
    sumnum.append(resultssum)


#将结果插入数据库
db=pymysql.connect(host="localhost",port=3306,user="root",passwd="123",db="echarts",charset="utf8")
cursor=db.cursor()

for row in sumnum:
    try:
        sql="insert into double_balls(numbers) values('%d')" %(row)
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
db.close()    


    
    
#tongji=defaultdict(list)
#for row in sumnum:
#    haoma=row
#    tongji[haoma].append(haoma)
#for haoma in tongji:
#    print (len(tongji[haoma]), " ".join(tongji[haoma]))
#print(sumnum)


    

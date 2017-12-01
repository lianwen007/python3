import pymysql
import matplotlib.pyplot as plt

db=pymysql.connect(host="localhost",port=3306,user="root",passwd="123",db="echarts",charset="utf8")
cursor=db.cursor()
sql="SELECT DISTINCT numbers,count(numbers)AS numcount FROM double_balls group BY numbers"
numberall=[]
cnumall=[]
try:
    cursor.execute(sql)
    results=cursor.fetchall()
    for row in results:
        numbers=row[0]
        numcount=row[1]
       # print("numbers=%s,numcount=%s" % (numbers,numcount))
        numberall.append(numbers)
        cnumall.append(numcount)
except:
    print("Error")
db.close()  

plt.scatter(numberall,cnumall,s=1)

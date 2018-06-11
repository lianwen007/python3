import time
from impala.dbapi import connect
sta = time.time()
print(sta)
a='aaa'
b='bbb'
c=1500000000
d=[('ddd','eee','1000000'),('fff','ggg','12344444'),('aaa','ddd','123111333')]
test_data = []
for i in range(10):
    value = ('test',str(i**2),str(i))
    test_data.append(value)
conn = connect(host='172.16.30.38',database='temp', port=10000, auth_mechanism='PLAIN' ) #21050)
#conn = connect(host='nat.yunzuoye.net', port=6667)
cur = conn.cursor()
insert_sql = "Insert into insert_test values (%s,%s,%s)"
cur.executemany(insert_sql,test_data)

cur.close()
conn.close()
end = time.time()
print(end-sta)

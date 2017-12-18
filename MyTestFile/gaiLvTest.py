"""
概率题一共八位数，由0-9组成，可重复，
首位数字可为0 问 
数字包含1，2，3，4，5 的概率是多少？
"""


import time
start = time.clock()

y=[1,2,3,4,5]
allnum=10**8
sumnum=0
for x in range(allnum):
    s = '0'*(8-len(str(x)))+str(x)   
    if '1' in s and '2' in s and '3' in s and '4' in s and '5' in s:
        sumnum+=1
print(sumnum/allnum)


elapsed = (time.clock() - start)
print("Time used:",elapsed)

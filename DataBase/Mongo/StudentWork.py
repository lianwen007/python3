import pymongo as pm
import json
import datetime

client=pm.MongoClient('192.168.5.52',50000)
db=client.xh_cloudwork

ressearch=db.studentWork.find_one()
for a,b in ressearch.items():
    st10=0
    if a=='userId':
        st1=b 
    elif a=='subject':
        st2=b
    elif a=='costTime':
        st3=b        
    elif a=='selfScore':
        st4=b 
    elif a=='score':
        st5=b 
    elif a=='topicNum':
        st6=b 
    elif a=='workFlag':
        st7=b 
    elif a=='wrongNum':
        st9=b 
    elif a=='lectureTimes':
        for c in b:
            st10+=b['listenTimes']
    elif a=='schedule':
        st11=b
    elif a=='workId':
        st12=b
    elif a=='createTime':
        st13=b
    elif a=='handInTime':
        st14=b
mess=str(st1)+'\tyunzuoye'+'\t'+str(st2)+'\t'+str(st3)+'\t'+str(st12)+'\t'\
    +str(st4)+'\t'+str(st5)+'\t'+str(st6)+'\t'+str(st7)+'\t'\
    +str(st6-st9)+'\t'+str(st9)+'\t'+str(st10)+'\t'+str(st11)\
    +'\t'+str(st13)+'\t'+str(st14)+'\t'+'2017-01-11'+'\n'
fileObject = open('F:\StudentWork.txt', 'a')
fileObject.write(mess)
fileObject.close()

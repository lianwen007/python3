import pymongo as pm
import datetime

client=pm.MongoClient('192.168.5.52',50000)
db=client.king
startedtime = datetime.datetime.now()
ressearch=db.homeWork.find()
fileObject = open('F:\StudentWork.txt', 'a')
finValue=[]
for ress in ressearch:
    values=[]
    values.append(str(ress['homeWorkId']))
    values.append(str(ress['createTime']))
    values.append(str(ress['studentId']))
    values.append(str(ress['teacherId']))
    values.append(str(ress['bookId']))
    values.append(str(ress['gameCount']))
    values.append(str(ress['finishCount']))
    values.append(str(ress['isFinish']))
    values.append(str(ress['updateTime']))
    messes='\t'.join(values)+'\n'
    fileObject.write(messes)
#datas='\n'.join(finValue)

fileObject.close()

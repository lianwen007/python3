import pymongo as pm
import datetime,time

sta =  time.time()
client=pm.MongoClient('192.168.5.52',50000)
db=client.king
startedtime = datetime.datetime.now()
ressearch=db.game.find()
#fileObject = open('/root/studentWork.txt', 'a')
fileObject = open('f:\\studentWork.txt', 'a')
for ress in ressearch:
    values=[]
    values.append(str(ress['_id']))
    if ress.get('homeWorkId'):
        values.append(str(ress['homeWorkId']))
    else:
        values.append('0')
    if ress.get('questionType'):
        values.append(str(ress['questionType']))
    else:
        values.append('0')
    messes='\t'.join(values)+'\n'
    fileObject.write(messes)
#datas='\n'.join(finValue)

fileObject.close()
end=time.time()
print(end-sta)

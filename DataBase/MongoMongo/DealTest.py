import pymongo as pm

client=pm.MongoClient('192.168.47.128',27017)
db=client.test01

datas=db.col.find()

for data in datas:
    print(data)

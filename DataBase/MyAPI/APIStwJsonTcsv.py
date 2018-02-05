# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 16:39:12 2018

@author: Administrator
"""
from flask import Flask,request,make_response
import json
import csv

app = Flask(__name__)#创建一个服务，赋值给APP
#json_str = '[{"classid": 4383, "topicnum": 10, "schoolid": 3495, "classname": "903", "numselfwork": 1, "hp": 3, "datetime": "2018-02-01", "bookname": "数学刷题王精品题库七上（ZJ）", "bookid": "5a2e4ac62c8afb18e6708fba", "schoolname": "象山县荔港学校", "credit": 26, "counttime": 486, "numhomework": 0, "username": "郑露露", "countscore": 21.0, "userid": 32099, "countright": 7, "rightlv": 0.699999988079071}, {"classid": 4383, "topicnum": 10, "schoolid": 3495, "classname": "903", "numselfwork": 1, "hp": 3, "datetime": "2018-02-01", "bookname": "科学刷题王精品题库七上（ZJ）", "bookid": "5a2f35632c8afb18e670b0c9", "schoolname": "象山县荔港学校", "credit": 26, "counttime": 272, "numhomework": 0, "username": "郑露露", "countscore": 27.0, "userid": 32099, "countright": 9, "rightlv": 0.8999999761581421}, {"classid": 4383, "topicnum": 10, "schoolid": 3495, "classname": "903", "numselfwork": 1, "hp": 13, "datetime": "2018-02-01", "bookname": "科学刷题王精品题库七上（ZJ）", "bookid": "5a2f35632c8afb18e670b0c9", "schoolname": "象山县荔港学校", "credit": 35, "counttime": 485, "numhomework": 0, "username": "刘晓城", "countscore": 24.0, "userid": 32102, "countright": 5, "rightlv": 0.5}, {"classid": 4766, "topicnum": 40, "schoolid": 760, "classname": "901", "numselfwork": 4, "hp": 4, "datetime": "2018-02-01", "bookname": "数学中考寒假刷题王", "bookid": "5a698ec0363d78315d2e49c8", "schoolname": "海宁宏达中学", "credit": 75, "counttime": 3883, "numhomework": 0, "username": "吕江涛", "countscore": 111.0, "userid": 50374, "countright": 37, "rightlv": 0.925000011920929}, {"classid": 4766, "topicnum": 20, "schoolid": 760, "classname": "901", "numselfwork": 2, "hp": 10, "datetime": "2018-02-01", "bookname": "数学中考寒假刷题王", "bookid": "5a698ec0363d78315d2e49c8", "schoolname": "海宁宏达中学", "credit": 60, "counttime": 2063, "numhomework": 0, "username": "金雨晴", "countscore": 60.0, "userid": 50392, "countright": 20, "rightlv": 1.0}, {"classid": 4766, "topicnum": 10, "schoolid": 760, "classname": "901", "numselfwork": 1, "hp": 5, "datetime": "2018-02-01", "bookname": "数学中考寒假刷题王", "bookid": "5a698ec0363d78315d2e49c8", "schoolname": "海宁宏达中学", "credit": 35, "counttime": 1651, "numhomework": 0, "username": "吕丹阳", "countscore": 30.0, "userid": 50393, "countright": 10, "rightlv": 1.0}, {"classid": 4766, "topicnum": 10, "schoolid": 760, "classname": "901", "numselfwork": 1, "hp": 4, "datetime": "2018-02-01", "bookname": "数学中考寒假刷题王", "bookid": "5a698ec0363d78315d2e49c8", "schoolname": "海宁宏达中学", "credit": 36, "counttime": 1889, "numhomework": 0, "username": "张怡婷", "countscore": 30.0, "userid": 50403, "countright": 10, "rightlv": 1.0}, {"classid": 4766, "topicnum": 10, "schoolid": 760, "classname": "901", "numselfwork": 1, "hp": 4, "datetime": "2018-02-01", "bookname": "数学中考寒假刷题王", "bookid": "5a698ec0363d78315d2e49c8", "schoolname": "海宁宏达中学", "credit": 34, "counttime": 1352, "numhomework": 0, "username": "朱鑫雅", "countscore": 24.0, "userid": 50406, "countright": 7, "rightlv": 0.699999988079071}, {"classid": 4767, "topicnum": 10, "schoolid": 760, "classname": "902", "numselfwork": 1, "hp": 5, "datetime": "2018-02-01", "bookname": "数学中考寒假刷题王", "bookid": "5a698ec0363d78315d2e49c8", "schoolname": "海宁宏达中学", "credit": 34, "counttime": 1369, "numhomework": 0, "username": "曾家乐", "countscore": 27.0, "userid": 50408, "countright": 9, "rightlv": 0.8999999761581421}, {"classid": 4767, "topicnum": 10, "schoolid": 760, "classname": "902", "numselfwork": 1, "hp": 12, "datetime": "2018-02-01", "bookname": "科学中考寒假刷题王", "bookid": "5a685349363d78315d2e0307", "schoolname": "海宁宏达中学", "credit": 28, "counttime": 220, "numhomework": 0, "username": "吴周毅", "countscore": 30.0, "userid": 50419, "countright": 10, "rightlv": 1.0}, {"classid": 4767, "topicnum": 20, "schoolid": 760, "classname": "902", "numselfwork": 2, "hp": 7, "datetime": "2018-02-01", "bookname": "数学中考寒假刷题王", "bookid": "5a698ec0363d78315d2e49c8", "schoolname": "海宁宏达中学", "credit": 36, "counttime": 2813, "numhomework": 0, "username": "张铭洋", "countscore": 42.0, "userid": 50423, "countright": 14, "rightlv": 0.699999988079071}]'

@app.route('/bigdata/product_stw/jsontocsv',methods=['post'])    
def get_userinfo():
    stwdata=request.values.get('stwdata')
    #schoolid = str(request.json.get('schoolid')) #获取带json串请求的userid参数传入的值
    s=Tranjsoncsv(stwdata)#(str(stwdata))
    content=s.jsontocsv()
    response = make_response(content)
    response.headers["Content-Type"] ="text/html; charset=gb2312"
    response.headers["Content-Disposition"] = "attachment; filename=Stwdata.csv;"
    return response

class Tranjsoncsv(object):
    def __init__(self,jsonstr):
        self.jsonstr=jsonstr
    
    def jsontocsv(self):
        val,val2='',''
        valuename=['schoolid','schoolname','bookname','classname','username','hp','credit','countscore','numhomework','numselfwork','topicnum','countright','rightlv','counttime']
        valuenamechn=['学校ID','学校名称','书名','班级','姓名','体力','诚信分','积分','作业次数','自练次数','做题量','正确地梁','正确率','平均做题时间(秒)']
        jsonvalues=json.loads(self.jsonstr)
        #for keyname in jsonvalues[0].keys():
        #    data.append(keyname)    
        for vals in jsonvalues:
            data=[]
            for x in valuename:
                data.append(str(vals[x]))
            val=','.join(data)
            val2=val2+val+'\n'
            datav = ','.join(valuename)+'\n'+val2
        return datav.encode('gb2312')
        
app.run(host='0.0.0.0'port=18890,debug=True,threaded=True) 

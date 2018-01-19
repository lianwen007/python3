from flask import Flask,request
import pymysql
import json

app = Flask(__name__)#创建一个服务，赋值给APP
@app.route('/get_user',methods=['get'])#指定接口访问的路径，支持什么请求方式get，post
def get_ss():
    userid = request.args.get('userid')#使用request.args.get方式获取拼接的入参数据
    data=get_mysql_conn(userid)
    return data

def get_mysql_conn(userid=''):
    db=pymysql.connect(host="localhost",port=3306,
                       user="root",passwd="123",db="elasticsearch",charset="utf8")
    cursor=db.cursor()
    sql="SELECT * FROM user_file_product WHERE userid = %s"%(userid)
    mess={}
    try:
        cursor.execute(sql)
        results=cursor.fetchone()
        mess['id']=results[0]
        mess['userid']=results[1]
        mess['username']=results[2]
        mess['schoolid']=results[3]
        mess['schoolname']=results[4]
        mess['gradename']=results[5]
        mess['scorestatus']=results[6]
        mess['scorechn']=results[7]
        mess['rankchn']=results[8]
        mess['scoremath']=results[9]
        mess['rankmath']=results[10]
        mess['scoreeng']=results[11]
        mess['rankeng']=results[12]
        mess['scoresci']=results[13]
        mess['ranksci']=results[14]
        mess['avgstatus']=results[15]
        mess['topstatus']=results[16]
        mess['topnumber']=results[17]
        mess['finalstatus']=results[18]
        mess['datetime']=results[19]
    except:
        mess['error']=404
    db.close()
    return json.dumps(mess)
    
app.run(host='0.0.0.0',port=8802,debug=Tr

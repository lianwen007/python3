from flask import Flask,jsonify,request
data = {'huhy':{'age':24,'sex':'女'},
        'liuer':{'age':12,'sex':'男'}
        }
err = {'zz':404,
       'yy':502
       }
app = Flask(__name__)#创建一个服务，赋值给APP
@app.route('/get_user',methods=['get'])#指定接口访问的路径，支持什么请求方式get，post

#请求后直接拼接入参方式
def get_ss():
    username = request.args.get('username')#使用request.args.get方式获取拼接的入参数据
    if username in data:  # 判断请求传入的参数是否在字典里
        return jsonify(data[username])
	#如果在的话，则返回data对应key的值转成的json串信息
    else:
        return jsonify(err[username])
	#如果不在的话，返回err对应key的value转成的json串信息
app.run(host='0.0.0.0',port=8802,debug=True)

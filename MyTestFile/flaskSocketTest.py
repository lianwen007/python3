from flask import Flask
from flask_sockets import Sockets
import datetime
import time
import random


app = Flask(__name__)
sockets = Sockets(app)


@sockets.route('/echo')
def echo_socket(ws):
    while not ws.closed:

        now = datetime.datetime.now().isoformat() + 'Z'
        ws.send(now)  #发送数据
        time.sleep(1)


@app.route('/')
def hello():
    return 'Hello World!'


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    print('server start')
    server.serve_forever()
    
    
   """
   <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="https://cdn.bootcss.com/jquery/3.2.0/jquery.js"></script>
</head>
<body>
    <div id="time" style="width: 300px;height: 50px;background-color: #0C0C0C;
    color: white;text-align: center;line-height: 50px;margin-left: 40%;font-size: 20px"></div>

    <script>
            var ws = new WebSocket("ws://127.0.0.1:5000/echo");

            ws.onmessage = function (event) {
                content = document.createTextNode(event.data);
                $("#time").html(content);

            };

    </script>
    </body>
</html>
"""

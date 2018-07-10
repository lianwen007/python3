import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders


# server['name'], server['user'], server['passwd']
_default_server = {'name': 'smtp.mxhichina.com',  'user': 'bigdata@quuedu.com', 'password': 'XXXXXXXXX'}


def send_mail(server=_default_server, to_name=list(), subject="", html_text="", files=list()):

    msg = MIMEMultipart()
    msg['From'] = server['user']  # 邮件的发件人
    msg['Subject'] = subject  # 邮件的主题
    msg['To'] = COMMASPACE.join(to_name)  # COMMASPACE==', ' 收件人可以是多个，to是一个列表
    msg['Date'] = formatdate(localtime=True)  # 发送时间，当不设定时，用outlook收邮件会不显示日期，QQ网页邮箱会显示日期
    # MIMIMEText有三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码，二和三可以省略不写
    # msg.attach(MIMEText(text, 'plain', 'utf-8'))
    msg.attach(MIMEText(html_text, 'html', 'utf-8'))

    for file in files:  # 添加附件可以是多个，files是一个列表，可以为空
        part = MIMEBase('application', 'octet-stream')  # 'octet-stream': binary data
        with open(file, 'rb') as f:
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
        msg.attach(part)

    # smtp = smtplib.SMTP()
    smtp = smtplib.SMTP_SSL()  # 使用SSL的方式去登录(例如QQ邮箱，端口是465)
    smtp.connect(server['name'])  # connect有两个参数，第一个为邮件服务器，第二个为端口，默认是25
    smtp.login(server['user'], server['password'])  # 用户名，密码
    smtp.sendmail(server['user'], to_name, msg.as_string())  # 发件人，收件人，发送信息
    smtp.close()  # 关闭连接


if __name__ == '__main__':
    name_to = ['XXXXXXXXXXX']
    subject_to = 'test002'
    html_txt = '''BigDataTest'''
    send_mail(_default_server, name_to, subject_to, html_txt)

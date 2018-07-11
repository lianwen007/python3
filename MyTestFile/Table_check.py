import os
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy import create_engine

sched = BackgroundScheduler()
trigger = CronTrigger(hour='8', minute='0', day='*')

# server['name'], server['user'], server['passwd']
_default_server = {'name': 'smtp.mxhichina.com',  'user': 'bigdata@quuedu.com', 'password': 'lwc123***'}


def send_mail(server=_default_server, to_name=list(), 
              subject="", html_text="", files=list()):
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

    smtp = smtplib.SMTP()
    #smtp = smtplib.SMTP_SSL()  # 使用SSL的方式去登录(例如QQ邮箱，端口是465)
    smtp.connect(server['name'])  # connect有两个参数，第一个为邮件服务器，第二个为端口，默认是25
    smtp.login(server['user'], server['password'])  # 用户名，密码
    smtp.sendmail(server['user'], to_name, msg.as_string())  # 发件人，收件人，发送信息
    smtp.close()  # 关闭连接


def get_base_info():
    base_list = list()
    db_table_list = list()
    cur = get_mysql_connect(db_name='elasticsearch')
    sql = 'select * from table_check_base_info'
    try:
        results = cur.execute(sql).fetchall()
    except Exception as e:
        results = tuple()
    for r in results:
        base_list.append(r)
        db_table_list.append(r[1:4])
    return base_list

    
def get_user_email():
    mail_list = list()
    cur = get_mysql_connect(db_name='elasticsearch')
    sql = 'select user_mail from table_check_mail_to'
    try:
        results = cur.execute(sql).fetchall()
    except Exception as e:
        results = tuple()
    for r in results:
        mail_list.append(r[0])
    return mail_list
    
    
def get_mysql_connect(port='3306',db_name=''):
    if db_name == 'xh_xueqing':
        host_name = '172.16.30.54'
        user_name = 'bigdatauser'
        passwd = 'Bigdata@321'
    elif db_name == 'xh_elasticsearch':
        host_name = '172.16.10.26'
        user_name = 'xhelas'
        passwd = 'Ma0Zy6P0'
    else:
        host_name = 'localhost'
        user_name = 'root'
        passwd = '123'
    engine_url = "mysql+pymysql://%s:%s@%s:3306/%s?charset=utf8"\
                           %(user_name,passwd,host_name,db_name)
    engine = create_engine(engine_url)
    # db = pymysql.connect(host_name, user_name, passwd, db_name,charset='utf8')
    # cur = engine.cursor()
    return engine

#sql = 'select src_file_day from product_stw_encount order by src_file_day desc'
def check_table_date(db_name,table_name,check_word):
    cur = get_mysql_connect(db_name=db_name)
    sql = 'select %s from %s order by %s desc' %(check_word,table_name,check_word)
    try:
        results = cur.execute(sql).fetchone()
    except Exception as e:
        results = tuple()
    check_result = ''
    if results:
        check_result = results[0]
    return check_result

    
def fill_html_text(html_title='大数据定时巡检 ',
                   html_th='<th>a</th>',
                   html_td='<tr> <td>b</td><td>c</td> </tr>'): 
    today_date = time.strftime('%Y%m%d')
    html_text = """
    <html>
    <body>
    <table border="1" cellpadding="10">
    <caption>(%s日期：%s)</caption>
      <tr>
        %s
      </tr>
        %s
    </table>
    </body>
    """%(html_title,today_date,html_th,html_td)
    return html_text

#@sched.scheduled_job(trigger)
def deal_main(max_works=10):
    base_values = get_base_info()
    html_td_end = ''
    today_date = time.strftime('%Y%m%d')
    with ThreadPoolExecutor(max_workers=max_works) as executor:
        for base_value in base_values:
            check_date = executor.submit(check_table_date,base_value[1],
                                         base_value[2],base_value[3]).result()
            want_date = str(int(today_date) + int(base_value[7]))
            if str(check_date) == want_date:
                html_date = '<td bgcolor="#009933" >%s</td>' %check_date
            else:
                html_date = '<td bgcolor="red">%s</td>' %check_date
            html_td = '<td>%s</td><td>%s</td><td>%s</td><td>%s</td>\
                        <td>%s</td>%s<td>%s</td>'\
                        %(base_value[4],base_value[1],base_value[2],base_value[5],
                          base_value[6],html_date,want_date)
            html_td_v = '<tr> %s </tr>' %html_td
            html_td_end += html_td_v
    html_th_end = '<th>产品/报表</th><th>数据库</th><th>数据表</th>\
                    <th>频率</th><th>优先级</th><th>数据日期</th><th>期望日期</th>'
    html_end = fill_html_text(html_td=html_td_end,html_th=html_th_end)
    user_email = get_user_email()
    subject_title = '大数据定时巡检%s' %today_date
    send_mail(to_name=user_email,subject=subject_title,html_text=html_end)
    print(html_end)
    return 1
#sched.start()


#@sched.scheduled_job(trigger)
#def thread_deal(max_works=10):
#    base_values, db_tables = get_base_info()
#    start_time = time.time()
#    with ThreadPoolExecutor(max_workers=max_works) as executor:
#        for base_value in base_values:
#            html_td_v = ''
#            for v in vase_value:
#                html_td = '<td>%s</td>'%(v)
#                html_td_v += html_td
#            
#            
#        future_task = executor.submit(self.mongo_to_txt, ex_path_name, skip_num)
#        if future_task.running():
#            set_log('%s is running' % str(future_task))
#    end_time = time.time()
#    return 1
    
    
    
#if __name__ == '__main__':
#    name_to = ['443129953@qq.com','lwc@quuedu.com']
#    subject_to = 'test002'
#    html_txt = fill_html_text()
#    send_mail(_default_server, name_to, subject_to, html_txt)

# -*- coding: utf-8 -*-
"""
Created on Thu Dec 27 15:55:25 2018

@author: Administrator
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import time
import requests
import json

sched = BackgroundScheduler()
trigger_every_second = CronTrigger(hour='*', minute='*', second='*/1')
trigger_every_3second = CronTrigger(hour='*', minute='*', second='*/3')


def send_msg2(t, url, at_all=False, mobiles=[]):
    dd_content = {
        "at": {
            "atMobiles": [str(m) for m in list(mobiles)],
            "isAtAll": at_all
        },    
        "msgtype": "text",
        
        "text": {
            "content": t
        }
    }
    print(dd_content)
    try:
        print(requests.post(url, data=json.dumps(dd_content), headers={'content-type': 'application/json'}).text)
    except:
        print("error")
        
@sched.scheduled_job(trigger_every_second)
@sched.scheduled_job(trigger_every_3second)
def send_test():
    print(time.time())

sched.start()

# sched.shutdown()

t="I am Rob! You can ask me some questions."

url="https://oapi.dingtalk.com/robot/send?access_token=c3927f6af7718928b8bc05bd92282502c6072ddcaeac04d005555cc9983939d4"

# send_msg2("Oh sorry! I don't have this skill too.",url)

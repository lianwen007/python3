import time
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

def myjob():
    print('job run at %s' % datetime.now())

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    trigger1 = CronTrigger(hour='*', minute='*', second='*/3')
    trigger2 = CronTrigger(hour='*', minute='*', second='*/5')
    job = scheduler.add_job(myjob, MultiCronTrigger([trigger1, trigger2]))
    scheduler.start()

try:
    while True:
        time.sleep(5)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()

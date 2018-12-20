from flask import Flask, url_for, request, redirect, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

sched = BackgroundScheduler()
trigger = CronTrigger(hour='0', minute='5')
app = Flask(__name__)
app.config.from_object('config')

# db = SQLAlchemy(app)
from app import views
sched.start()
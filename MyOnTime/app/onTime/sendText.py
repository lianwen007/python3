from flask import Blueprint, render_template, redirect,request,jsonify
from app import app
from app import sched


@sched.scheduled_job('cron', hour=0, minute=5, id='on_time_etl')
# @sched.scheduled_job('cron', second='*/3', id='on_time_etl_first')
def on_time_etl():
    pass


def send_mess():
    pass


sched.start()
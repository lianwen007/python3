from flask import Blueprint, render_template, redirect,request,jsonify
from app import app
from app import sched
from app.etlMongo.pubFunction import set_log
from app.etlMongo.tabStudent import get_stu_info
from app.etlMongo.tabHomework import get_homework
from app.etlMongo.tabGame import get_game_info
from .shellPy import data_etl_ext
import datetime
import time

getEtl = Blueprint('getEtl', __name__)


def getTraceId():
    import uuid
    return str(uuid.uuid1()).replace('-', '')


@getEtl.route('/etlTest/gettest', methods=['GET'])
def etl_test():
    # print('aaaTestNow is %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    datas = {'msg': 'Successful!'}
    return jsonify(datas)


@getEtl.route('/etlStudent', methods=['GET'])
def etl_student():
    password = request.values.get('password')
    start_time = time.time()
    if password == 'bigdata123':
        get_stu_info()
        datas = {'msg': 'Succeed to import table of student!'}
    else:
        datas = {'msg': 'Error, Password was wrong!'}
    end_time = time.time()
    finish_time = start_time - end_time
    set_log('etlStudent-', str(finish_time))
    return jsonify(datas)


@getEtl.route('/etlHomework', methods=['GET'])
def etl_homework():
    password = request.values.get('password')
    start_time = time.time()
    if password == 'bigdata123':
        get_homework()
        datas = {'msg': 'Succeed to import table of homework!'}
    else:
        datas = {'msg': 'Error, Password was wrong!'}
    end_time = time.time()
    finish_time = start_time - end_time
    set_log('etlHomework-', str(finish_time))
    return jsonify(datas)


@getEtl.route('/etlGame', methods=['GET'])
def etl_game():
    password = request.values.get('password')
    start_time = time.time()
    if password == 'bigdata123':
        get_game_info()
        datas = {'msg': 'Succeed to import table of homework!'}
    else:
        datas = {'msg': 'Error, Password was wrong!'}
    end_time = time.time()
    finish_time = start_time - end_time
    set_log('etlGame-', str(finish_time))
    return jsonify(datas)


@sched.scheduled_job('cron', hour=0, minute=5, id='on_time_etl')
# @sched.scheduled_job('cron', second='*/3', id='on_time_etl_first')
def on_time_etl():
    start_time = time.time()

    get_stu_info()
    get_homework()
    get_game_info()
    etl_result = 0  # data_etl_ext()

    end_time = time.time()
    finish_time = start_time - end_time
    log_info = 'Code['+etl_result+']TimeCost['+str(finish_time)+']'
    set_log('etlAutoTable-', log_info)

sched.start()

from .pubFunction import *
from config import etl_root_path
import time


def get_homework():
    db = mongo_client()
    results = db.student.find()
    dt = set_time_path()
    file_path = etl_root_path + '/homework/stw_homework_{}.txt'.format(dt)
    fileObject = open(file_path, 'a')
    for result in results:
        values = list()
        values.append(str(result['_id']))
        values.append(str(result['homeWorkId']))
        values.append(str(result['createTime']))
        values.append(str(result['studentId']))
        values.append(str(result['teacherId']))
        values.append(str(result['bookId']))
        values.append(str(result['gameCount']))
        values.append(str(result['finishCount']))
        values.append(str(result['isFinish']))
        values.append(str(result['updateTime']))
        messes = '\t'.join(values) + '\n'
        fileObject.write(messes)
    fileObject.close()
    end = time.time()


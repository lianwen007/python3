from .pubFunction import *
from config import etl_root_path
import time


def get_stu_info():
    db = mongo_client()
    results = db.student.find()
    dt = set_time_path()
    file_path = etl_root_path + '/stuinfo/stw_student_{}.txt'.format(dt)
    fileObject = open(file_path, 'a')
    for result in results:
        values = list()
        values.append(str(result['studentId']))
        values.append(str(result['studentName']))
        values.append(str(result['classId']))
        values.append(str(result['className']))
        values.append(str(result['schoolId']))
        values.append(str(result['schoolName']))
        values.append(str(result['hp']))
        values.append(str(result['credit']))
        messes = '\t'.join(values) + '\n'
        fileObject.write(messes)
    fileObject.close()





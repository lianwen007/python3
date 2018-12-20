from .pubFunction import *
from config import etl_root_path
import time


def get_game_info():
    db = mongo_client()
    results = db.game.find()
    dt = set_time_path()
    file_path = etl_root_path + '/gameinfo/stw_game_{}.txt'.format(dt)
    fileObject = open(file_path, 'a')
    for result in results:
        udatetime = int(time.time())
        values = list()
        values.append(str(result['_id']))
        values.append(str(result['studentId']))
        values.append(str(result['bookId']))
        values.append(str(result['createTime']))
        values.append(str(result['updateTime']))
        if result.get('judgeCount'):
            if result['judgeCount'] > 10: result['judgeCount'] = 10
            values.append(str(result.get('judgeCount', 0)))
        elif not result.get('judgeCount'):
            values.append(str(result.get('accuracy', 0)))
        values.append(str(result.get('newIntegral', 0)))
        values.append(str(result['isHomeWork']))
        values.append(str(result.get('questionRight', result.get('failCount', 0))))
        values.append(str(result['timeConsuming']))
        values.append(str(udatetime))
        messes = '\t'.join(values) + '\n'
        fileObject.write(messes)
    fileObject.close()

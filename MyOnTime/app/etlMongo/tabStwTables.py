from .mainFunc import MongoEtlThread
from config import etl_root_path

_collection_name = 'xh_king'


def get_homework():
    local_table_name = 'homeWork'
    export_path_name = '{}{}/'.format(etl_root_path, local_table_name)
    local_values = ('_id', 'studentName', 'studentId', 'subjectId', 'type', 'countScore', 'teacherId', 'teacherName',
                    'homeWorkId', 'gameCount', 'finishCount', 'bookId', 'bookName', 'isFinish', 'accuracy')
    deal_main = MongoEtlThread(collection_name=_collection_name, root_path=export_path_name,
                               table_name=local_table_name, values_get=local_values)
    deal_main.thread_deal()
    

def get_game_info():
    local_table_name = 'game'
    export_path_name = '{}{}/'.format(etl_root_path, local_table_name)
    local_values = ('_id', 'studentId', 'bookId', 'createTime', 'updateTime', 'judgeCount', 'integral', 'newIntegral',
                    'isHomeWork', 'homeWorkId', 'questionRight', 'timeConsuming', 'failCount', 'accuracy',
                    'questionType', 'subjectId')
    deal_main = MongoEtlThread(collection_name=_collection_name, root_path=export_path_name,
                               table_name=local_table_name, values_get=local_values)
    deal_main.thread_deal()


def get_book_info():
    local_table_name = 'libraryBook'
    export_path_name = '{}{}/'.format(etl_root_path, local_table_name)
    local_values = ('bookId', 'bookName', 'count', 'subjectId', 'type', 'updateTime')
    deal_main = MongoEtlThread(collection_name=_collection_name, root_path=export_path_name,
                               table_name=local_table_name, values_get=local_values)
    deal_main.thread_deal()


def get_stu_info():
    local_table_name = 'student'
    export_path_name = '{}{}/'.format(etl_root_path, local_table_name)
    local_values = ('studentId', 'studentName', 'questionCount', 'hp', 'credit', 'questionRight', 'praiseCount',
                    'schoolId', 'schoolName', 'classId', 'className', 'enrollYear', 'grade', 'updateTime',)
    deal_main = MongoEtlThread(collection_name=_collection_name, root_path=export_path_name,
                               table_name=local_table_name, values_get=local_values)
    deal_main.thread_deal()

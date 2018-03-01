import time

log_config = {
    # 'file': 'logs/log.gua.txt'
}

def set_log_path():
    fmt = '%Y%m%d'# %H%M%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(fmt, value)
    log_config['file'] = '/work/serverpy/StwProject/logs/log.Stw.{}.txt'.format(dt)

def log(*args, **kwargs):
    # time.time() 返回 unix time
    # 如何把 unix time 转换为普通人类可以看懂的格式呢？
    fmt = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(fmt, value)
    # 这样确保了每次运行都有一个独立的 path 存放 log
    path = log_config.get('file')
    if path is None:
        set_log_path()
        path = log_config['file']
    with open(path, 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)

'''def log(*args, **kwargs):
    f = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(f, value)
    # 中文 windows 平台默认打开的文件编码是 gbk 所以需要指定一下
    with open('log.gua.txt', 'a', encoding='utf-8') as f:
        # 通过 file 参数可以把输出写入到文件 f 中
        # 需要注意的是 **kwargs 必须是最后一个参数
        print(dt, *args, file=f, **kwargs)'''
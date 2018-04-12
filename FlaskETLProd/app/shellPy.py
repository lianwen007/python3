from app.allCommands.allCommands import *
from app.allCommands.HiveQL import *


def ssh_command_ext(ext_command=''):
    # 远程执行shell命令，参数为命令字符串
    import paramiko
    import config
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # ssh连接配置在config中
    ssh.connect(hostname=config.ssh_hostname, port=config.ssh_port,
                username=config.ssh_username, password=config.ssh_password)
    stdin, stdout, stderr = ssh.exec_command(ext_command)
    cmd_result = stdout.readline()
    cmd_error = stderr.readline()
    ssh.close()
    if cmd_result:
        if not cmd_error:
            return 1
    return -1


def shell_command_data_load():
    # 按顺序执行依次，并验证执行的结果
    if ssh_command_ext(sqoop_import) == -1:
        return -1
    else:
        ssh_command_ext(mv_command)
        if ssh_command_ext(scp_command) == -1:
            return -2
        else:
            if ssh_command_ext(hive_table_truncate) == -1:
                return -3
            else:
                if ssh_command_ext(hive_table_load) == -1:
                    return -4
                else:
                    if ssh_command_ext(hive_table_insert) == -1:
                        return -5
    return 1


def shell_command_data_export():
    # 使用sqoop将数据导出到mysql
    if ssh_command_ext(sqoop_export) == 1:
        return 1
    return -1


def local_shell_ext(local_shell):
    # 本地shell命令执行，参数为命令
    import subprocess
    # FILE_PATH='e:\\111\\asdf\\123'  ###444.txt 不会当做文件，而是当做目录
    # if not os.path.exists(FILE_PATH):  ###判断文件是否存在，返回布尔值
    # os.makedirs(FILE_PATH)
    return subprocess.Popen(local_shell, shell=True)


def data_etl_ext():
    # ETL主函数
    local_shell_ext(local_mv_command)  # 先执行本地MV命令
    data_load_result = shell_command_data_load()
    if data_load_result == 1:
        export_data_result = shell_command_data_export()
        if export_data_result() == 1:
            return 1
        else:
            return export_data_result
    return data_load_result

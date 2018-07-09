def ssh_command_ext(ext_command=""):
    # 远程执行shell命令，参数为命令字符串
    import paramiko
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # ssh连接配置在config中
    ssh.connect(hostname="172.16.30.38", port=22,
                username="hadoop", password="hadoop!@#321")
    stdin, stdout, stderr = ssh.exec_command(ext_command)
    cmd_result = stdout.readline()
    cmd_error = stderr.readline()
    ssh.close()
    if cmd_result:
        print(cmd_result)
        if not cmd_error:
            return 1
    return -1


dt_array = list()
for i in range(29):
    if i < 9:
        dt = "2018-06-0" + str(i+1)
    else:
        dt = "2018-06-" + str(i+1)
    #dt_array.append(dt)
        
    hive_sql = """set dt_test=%s; select "${hiveconf:dt}"; """%dt
    cm_hive = "hive -e '%s'" %hive_sql
    ssh_command_ext(cm_hive)

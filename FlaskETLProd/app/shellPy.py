import paramiko

#FILE_PATH='e:\\111\\asdf\\123'  ###444.txt 不会当做文件，而是当做目录
#
#if not os.path.exists(FILE_PATH):  ###判断文件是否存在，返回布尔值
#   os.makedirs(FILE_PATH)


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='nat.yunzuoye.net', port=222, username='root', password='Big@2017')
memCmd = 'ls -l'
stdin, stdout, stderr = ssh.exec_command(memCmd)
memResult = stdout.read()

print(memResult)
#SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:123@localhost:3306/elasticsearch?charset=utf8'
CSRF_ENABLED = True
SECRET_KEY = 'Asd!23Asd!23'
#SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://webmail_user:szw_webmail1234@172.16.10.26:3306/xh_elasticsearch?charset=utf8'

SQLALCHEMY_TRACK_MODIFICATIONS = True

# mongo config
mongo_url = "192.168.5.52:50000"
etl_root_path = "/root/stwMongo/etl"
etl_log_path = "/root/stwMongo/etl_log"


# ssh address
ssh_hostname = 'nat.yunzuoye.net'
ssh_port = 222
ssh_username = 'root'
ssh_password = 'Big@2017'


# mysql config
mysql_config = {
    "hostname": "localhost",
    "port": 3306,
    "user": "root",
    "password": "123"
}


OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]

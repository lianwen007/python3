import pip
try:
    pip.main(['install','mysql-connector-python-rf'])
except:
    pip.main(['install', '-egg mysql-connector-python-rf'])
pip.main(['install','flask_sqlalchemy'])

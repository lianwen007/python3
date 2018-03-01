from app import app
from .getstwinfo import getstwinfo

app.register_blueprint(getstwinfo,url_prefix='')
#app.register_blueprint(user, url_prefix='/user')
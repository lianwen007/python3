from app import app
from .etlControl import getEtl


app.register_blueprint(getEtl, url_prefix='/bigdata/etlControl/getEtl')

#app.register_blueprint(user, url_prefix='/user')
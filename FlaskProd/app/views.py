from app import app
from .getStwInfo import getStwInfo
from .getKpiInfo import getKpiInfo
from .getEnStwInfo import getEnStwInfo

app.register_blueprint(getStwInfo,url_prefix='')
app.register_blueprint(getKpiInfo,url_prefix='')
app.register_blueprint(getEnStwInfo,url_prefix='')
#app.register_blueprint(user, url_prefix='/user')

from flask import Flask, url_for, request, redirect, render_template
from flask_cache import Cache
#from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_object('config')
cache=Cache(app, config={'CACHE_TYPE':'simple'})
#db = SQLAlchemy(app)
from app import models,views

from flask import Flask, url_for, request, redirect, render_template

app = Flask(__name__)
app.config.from_object('config')
from app import models,views
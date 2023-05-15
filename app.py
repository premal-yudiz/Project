from flask import Flask,redirect, render_template,request,url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__, template_folder='templete')
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite3'
db=SQLAlchemy(app)

with app.app_context():
    db.create_all()

from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.secret_key = 'abcd^&(JADJLFAIq128HADHJKvavnhae12345!@#$%'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/hoteldb?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

admin = Admin(app = app, name='My Hotel', template_mode='bootstrap4')
db = SQLAlchemy(app = app)
login = LoginManager(app=app)
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = "KRISHNA"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
##THIS IS A COMMAND FOR SQL to connext with XAMPP
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/fashion_classifier'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from fashion_classifier import routes


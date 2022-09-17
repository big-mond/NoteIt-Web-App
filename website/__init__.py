from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import datetime, timeago
from dotenv import load_dotenv
import os

#Environmental Table
load_dotenv()

db = SQLAlchemy()
DB_NAME = "database.db" 


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'os.getenv("SECRET_KEY")'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    db.init_app(app)

    #Template Fiters for date and time
    @app.template_filter('timeago')
    def fromnow(date):
     return timeago.format(date, datetime.datetime.now())
 
    @app.template_filter('datetime')
    def date_format(value):
        months = ('Jan','Feb',"Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec")
        month = months[value.month-1]
        hour = str(value.hour).zfill(2)
        minutes = str(value.minute).zfill(2)
        return "{} {} {} {}:{}hs".format(value.day, month, value.year, hour, minutes)
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    
    from .models import User, Note
    
    create_database(app)
    
    login_manager =LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
        
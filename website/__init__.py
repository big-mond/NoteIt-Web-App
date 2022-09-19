from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
#Login Handler
from flask_login import LoginManager
#Time Format
import datetime, timeago
#Environmental Table
from dotenv import load_dotenv


#Environmental Table
load_dotenv()

#Database
db = SQLAlchemy()
DB_NAME = "database.db" 

#App Config
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'os.getenv("SECRET_KEY")'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SECURITY_USER_IDENTITY_ATTRIBUTES'] = ('username', 'email')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    db.init_app(app)

    
    #Template Fiters for date and time
    @app.template_filter('timeago')
    def fromnow(date):
     return timeago.format(date, datetime.datetime.now())
    
    
    #Import Views and Auth settings
    from .views import views
    from .auth import auth
    
    #Register Views and Auth Blueprints
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    
    #Import Model classes for database 
    from .models import User
    
    #Create Database for app
    create_database(app)
    
    #Handles Login Settings
    login_manager =LoginManager()
    #Default View for Login
    login_manager.login_view = 'auth.login'
    #Start Login Manager with app
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
        
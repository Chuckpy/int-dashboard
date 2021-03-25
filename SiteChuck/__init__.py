from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME= "database.db"

#função para criação do banco com os modelos
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'NOSECRETKEYLOL'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)    

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Nota

    create_database(app)

    login_manager= LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)    
    login_manager.login_message = "Você precisa estar logado para acessar essa página"

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

#função para criar o banco caso ele não exista
def create_database(app):
    if not path.exists('SiteChuck/' + DB_NAME):
        db.create_all(app=app)
        print("Banco criado ! Olá mundo")

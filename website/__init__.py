from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os


db = SQLAlchemy()

bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = 'user.login'

mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']='0b70b35b6e09d382c506ec70983450e9'
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///website1.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
    app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    

    from website.main.routes import main
    from website.notes.routes import notes
    from website.user.routes import user
    from website.error.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(notes)
    app.register_blueprint(user)
    app.register_blueprint(errors)

    return app
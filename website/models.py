from flask_login import UserMixin
from sqlalchemy.sql import func
import jwt
from website import db, login_manager
from flask import current_app as app

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    imgfile = db.Column(db.String(20), default='default.jpg')
    notes = db.relationship('Note')
    #notes = db.relationship('Note', backref='author', lazy=True)
    #here backref is declared as a column in Note and can be referenced as Note while querying and lazy means optimized loading check web

    def get_reset_token(self, exp=1800):
        return jwt.encode({'user':self.email, 'exp':exp}, key=app.config['SECRET_KEY'], algorithm="HS256")

    def verify_token(token):
        try:
            user = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms="HS256")['user']
        except:
            return None
        return User.query.filter_by(email=user).first()

    #in django it is __str__ method
    def __repr__(self):
        return f"(User('{self.first_name}', '{self.last_name}', '{self.imgfile}')"


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(100000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #here user.id is small case because it is a column but the Note is a class above mentioned
from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model, UserMixin):
    """Model for a user who logs in to the app"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(128), index=True, unique=True)
    email_confirmed = db.Column(db.Boolean, default=False)
    messages = db.relationship('Message', backref='author', lazy='dynamic')
    channels = db.relationship('Channel', backref='creator', lazy='dynamic')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"{self.__class__.__name__}(username:{self.username})"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Channel(db.Model):
    """Model for where the chat channels are stored"""
    __tablename__ = 'channels'

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(64), index=True)
    posts = db.relationship('Message', backref='channel', lazy='dynamic')

    def __repr__(self):
        return f"{self.__class__.__name__}(channel name:{self.name})"


class Message(db.Model):
    """Model for where the chat channels are stored"""
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'))
    text = db.Column(db.String)

    def __repr__(self):
        return f"{self.__class__.__name__}(message body:{self.text})"

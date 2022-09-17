from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), default=datetime.datetime.now, onupdate=datetime.datetime.now)
    notes = db.relationship('Note', backref='user', passive_deletes=True)
    comments = db.relationship('Comment', backref='user', passive_deletes=True)
    

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), default=datetime.datetime.now, onupdate=datetime.datetime.now)
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    comments = db.relationship('Comment', backref='post', passive_deletes=True)
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), default=datetime.datetime.now, onupdate=datetime.datetime.now)
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id', ondelete="CASCADE"), nullable=False)
    
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')

    org_bool = db.Column(db.Integer)
    org_name = db.Column(db.String(150))
    org_types = db.Column(db.String(250))
    org_volunteers = db.Column(db.Integer)
    org_lat = db.Column(db.Float)
    org_long = db.Column(db.Float)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emailID = db.Column(db.String(100), unique=True)
    # emailID = db.Column(db.String(100))
    type = db.Column(db.String(200))
    lat = db.Column(db.Float)
    long = db.Column(db.Float)
    active = db.Column(db.Integer)
    time = db.Column(db.String(50))

    


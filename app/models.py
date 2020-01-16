from . import db,login_manager
from werkzeug import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin,db.Model):

    __tablename__ = 'users'

    id= db.Column(db.Integer,primary_key=True)
    email= db.Column(db.String(255),unique=True,nullable=False)
    name= db.Column(db.String(255),unique=True,nullable=False)
    password=db.Column(db.String(255),unique=True,nullable=False)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String)
    pitches = db.relationship('Pitch',backref='user',lazy='dynamic')
    comment = db.relationship('Comment',backref='user',lazy='dynamic')
    upvote = db.relationship('Upvote',backref='user',lazy='dynamic')
    downvote = db.relationship('Downvote',backref='user',lazy='dynamic') 


    @property
    def password(self):
        raise AttributeError ('you cannot review password attribute')
    

    @password.setter
    def password(self,password):
        self.secure_password=generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.secure_password,password)

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'User {self.name }'

class Pitch(db.Model):
    __tablename__= 'pitchez'

    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(255),nullable=False)
    post=db.Column(db.String,nullable=False)
    time=db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    category=db.Column(db.String(255),nullable=False,index=True)
    comment=db.relationship('Comment',backref='pitch',lazy='dynamic')
    upvote = db.relationship('Upvote',backref='pitch',lazy='dynamic')
    downvote = db.relationship('Downvote',backref='pitch',lazy='dynamic')


    def save_pitchez(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'Pitch {self.post}'

class Comment(db.Model):
    __tablename__ = 'comment'
    id=db.Column(db.Integer,primary_key=True,nullable=False)
    post=db.Column(db.String(255),nullable=False)
    time=db.Column(db.DateTime,default=datetime.utcnow)
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitchez.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,pitch_id):
        comments = Comment.query.filter_by(pitch_id=pitch_id).all()

    def __repr__(self):
        return f"comment:{self.comment}"

class Downvote(db.Model):
    __tablename__ = 'downvote'

    id=db.Column(db.Integer,primary_key=True,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitchez.id'))
    
    def save_dvote(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_downvotes(cls,id):
        downvote = Downvote.query.filter_by(pitch_id = id).all()
        return downvote

    def __repr__(self):
        return f"{self.user_id}:{self.pitch_id}"


class Upvote(db.Model):
    __tablename__= 'upvote'

    id=db.Column(db.Integer,primary_key=True,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitchez.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_upvotes(cls,id):
        upvote = Upvote.query.filter_by(pitch_id = id).all()
        return upvote

    def __repr__(self):
        return f"{self.user_id}:{self.pitch_id}"
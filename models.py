"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

DEFAULT_IMG = 'https://st3.depositphotos.com/4111759/13425/v/600/depositphotos_134255710-stock-illustration-avatar-vector-male-profile-gray.jpg'

class User(db.Model):
    """User."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key =True, autoincrement=True)

    first_name = db.Column(db.Text,nullable=False)

    last_name = db.Column(db.Text,nullable=False)

    image_url = db.Column(db.Text,nullable=False,default=DEFAULT_IMG)

    posts = db.relationship('Post',backref="user", cascade="all, delete-orphan")

    @property
    def full_name(self):
        """Returns full name of the user"""
        return f"{self.first_name} {self.last_name}"

class Post(db.Model):
    """Posts."""

    __tablename__ ='posts'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)

    title = db.Column(db.Text, nullable=False)

    content = db.Column(db.Text, nullable = False)

    created_at = db.Column(db.DateTime,nullable=False,default=datetime.datetime.now)

    user_id = db.Column(db.Integer,db.ForeignKey('users.id'), nullable = False)

    @property
    def friendly_date(self):
        """Returns nice looking date"""
        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")

        
def connect_db(app):
    """Conect to database"""
    db.app = app
    db.init_app(app)
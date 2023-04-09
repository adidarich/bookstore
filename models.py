from app import db
from flask_login import UserMixin
from sqlalchemy import func


class AddBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(80), unique=True, nullable=False)
    pl = db.Column(db.String(18), nullable=False)
    cover = db.Column(db.String(40), nullable=False, default='default')
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return self.cover, self.title, self.author


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(24), unique=True)
    first_name = db.Column(db.String(24))
    password = db.Column(db.String(50))
    books = db.relationship('AddBook')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __unicode__(self):
        return self.username

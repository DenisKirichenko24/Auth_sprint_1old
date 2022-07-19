from core.config import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'),
                        nullable=True)

    def __repr__(self):
        return '<User %r>' % self.username

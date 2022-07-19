from sqlalchemy import ForeignKey

from api.core.config import db
from api.models.users import User


class Session(db.Model):
    __tablename__ = 'session'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    login_time = db.Column(db.DateTime)

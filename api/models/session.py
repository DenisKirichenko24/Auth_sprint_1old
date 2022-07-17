from api.core.config import db
from users import User


class Session(db.Model):
    __tablename__ = 'session'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, foreign_key=User.id)
    login_time = db.Column(db.String(50), unique=True, nullable=False)

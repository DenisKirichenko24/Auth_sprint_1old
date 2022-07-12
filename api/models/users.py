from flask_login import UserMixin

from api.core.config import db, manager


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)


@manager.user_loader
def load_user(user_id):
    return User.get(user_id)

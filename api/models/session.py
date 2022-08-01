import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import UniqueConstraint
import enum
from sqlalchemy import ForeignKey

from core.config import db


class DeviceTypeEnum(enum.Enum):
    mobile = 'mobile'
    web = 'web'
    smart = 'smart'


def create_partition(target, connection, **kw) -> None:
    """ creating partition by session """
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "session_smart" 
        PARTITION OF "session" FOR VALUES IN ('smart')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "session_mobile" 
        PARTITION OF "session" FOR VALUES IN ('mobile')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "session_web" 
        PARTITION OF "session" FOR VALUES IN ('web')"""
    )


class Session(db.Model):
    __tablename__ = 'session'
    __table_args__ = (
        UniqueConstraint('id', 'user_device_type'),
        {
            'postgresql_partition_by': 'LIST (user_device_type)',
            'listeners': [('after_create', create_partition)],
        }
    )

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    login_time = db.Column(db.DateTime)
    user_agent = db.Column(db.Text)
    user_device_type = db.Column(db.Text, primary_key=True)

    def __repr__(self):
        return f'<UserSignIn {self.user_id}:{self.login_time}>'

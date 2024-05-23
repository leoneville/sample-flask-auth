from database import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    #id (int), username (str), password (str), role (str)
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(80), nullable=False, default='user')

    def to_dict(self):
        unprinted_attr = ["password"]
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name not in unprinted_attr}

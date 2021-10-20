from werkzeug.security import generate_password_hash, check_password_hash
from application.ext.database import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(86), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean)

    def __init__(self, username, password, is_admin = False):
        self.username = username
        self.is_admin = is_admin
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)
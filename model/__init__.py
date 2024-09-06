from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import (
    generate_password_hash, 
    check_password_hash
)
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        """Check if the provided password matches the stored hashed password."""
        return check_password_hash(self.password, password)

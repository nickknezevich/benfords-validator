from flask_sqlalchemy import SQLAlchemy
from . import db
import datetime
import jwt
import time
from werkzeug.security import generate_password_hash, check_password_hash

SECRET_KEY = '1234'
EXPIRES_IN = 900000000;   

class User(db.Model):
    """Data model for users."""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(80), index=True, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    # Define the one-to-many relationship with ValidationEntry
    validation_entries = db.relationship('ValidationEntry', backref='user', lazy=True)
    
    def hash_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)
    
    def generate_auth_token(self, expires_in = EXPIRES_IN):
        return jwt.encode(
            { 'id': self.id, 'exp': time.time() + expires_in }, 
            SECRET_KEY, algorithm='HS256')

    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(token, SECRET_KEY,
            algorithm=['HS256'])
        except:
            return 
        return User.query.get(data['id'])

class ValidationEntry(db.Model):
    """Data model for user validation_entres."""

    __tablename__ = "validation_entries"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    result = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
   

    def __repr__(self):
        return f'<ValidationEntry {self.id}>'
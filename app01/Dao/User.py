from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'User'
    UserID = db.Column('UserID', db.Integer, primary_key=True)
    Username = db.Column('Username', db.String(50))
    Password = db.Column('Password', db.String(100))
    Email = db.Column('Email', db.String(100))
    PhoneNumber = db.Column('PhoneNumber', db.String(20))
    Role = db.Column('Role', db.String(20))
    VerificationCode = db.Column('VerificationCode', db.String(20))
    RegistrationTime = db.Column('RegistrationTime', db.TIMESTAMP, default=db.func.current_timestamp())
    LastLoginTime = db.Column('LastLoginTime', db.TIMESTAMP)
    AccountStatus = db.Column('AccountStatus', db.String(20))
    
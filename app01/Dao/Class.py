from __init__ import db

class Class(db.Model):
    __tablename__ = 'Class'
    ClassID = db.Column('ClassID', db.Integer, primary_key=True)
    ClassName = db.Column('ClassName', db.String(100), nullable=False)

class ClassUser(db.Model):
    __tablename__ = 'class_user'
    ClassID = db.Column(db.Integer, db.ForeignKey('Class.ClassID'), primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('User.UserID'), primary_key=True)

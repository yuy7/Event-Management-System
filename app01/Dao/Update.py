from __init__ import db

class Update(db.Model):
    __tablename__ = 'update'
    UpdateID = db.Column('UpdateID', db.Integer, primary_key=True)
    LastLoginTime = db.Column('LastLoginTime', db.TIMESTAMP)
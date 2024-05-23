
from __init__ import db

class Location(db.Model):
    __tablename__ = 'location'
    
    locationId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.Integer, nullable=False)
    building = db.Column(db.Integer, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Integer, nullable=False)
    occupy = db.Column(db.VARCHAR(45), nullable=False)
from __init__ import db

class Event(db.Model):
    __tablename__ = 'Event'
    eventID = db.Column('eventID', db.Integer, primary_key=True)
    eventName = db.Column('eventName', db.String(45))
    eventStartDate = db.Column('eventStartDate', db.TIMESTAMP)
    eventEndDate = db.Column('eventEndDate', db.TIMESTAMP)
    eventLocation = db.Column('eventLocation', db.String(45))
    
    
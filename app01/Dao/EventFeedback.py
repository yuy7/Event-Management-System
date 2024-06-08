from __init__ import db

class EventFeedback(db.Model):
    __tablename__ = 'eventFeedback'
    
    feedbackId = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, nullable=False)
    eventID = db.Column(db.Integer, nullable=False)
    feedback = db.Column(db.String(1000), nullable=False)
    feedbackTime = db.Column(db.TIMESTAMP)

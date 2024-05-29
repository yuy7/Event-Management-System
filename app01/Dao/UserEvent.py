from __init__ import db

class UserEvent(db.Model):
    __tablename__ = 'user_event'
    userID = db.Column(db.Integer, db.ForeignKey('User.UserID'), primary_key=True)
    eventID = db.Column(db.Integer, db.ForeignKey('tempevent.eventID',primary_key=True))

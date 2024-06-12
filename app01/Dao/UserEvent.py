from __init__ import db

class UserEvent(db.Model):
    __tablename__ = 'user_event'
    userEventID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userID = db.Column(db.Integer, db.ForeignKey('User.UserID'))
    eventID = db.Column(db.Integer, db.ForeignKey('event.eventID'))

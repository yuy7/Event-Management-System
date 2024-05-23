from __init__ import db
from datetime import datetime

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column('id', db.Integer, primary_key=True)
    recipient_id = db.Column('recipient_id', db.Integer, db.ForeignKey('User.UserID'), nullable=False)
    sender_id = db.Column('sender_id', db.Integer, db.ForeignKey('User.UserID'), nullable=False)
    event_id = db.Column('event_id', db.Integer, db.ForeignKey('Event.eventID'), nullable=False)
    message = db.Column('message', db.String(255), nullable=False)
    read = db.Column('read', db.Boolean, default=False)
    timestamp = db.Column('timestamp', db.DateTime, default=datetime.utcnow)

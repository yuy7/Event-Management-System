from __init__ import db

class EventDetail(db.Model):
    __tablename__ = 'event_detail'
    detailID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    eventID = db.Column(db.Integer, db.ForeignKey('event.eventID'), nullable=False)
    description = db.Column(db.Text, nullable=True)
    notification = db.Column(db.Text, nullable=True)
    result = db.Column(db.Text, nullable=True) 

from __init__ import db

class TimeSlot(db.Model):
    __tablename__ = 'timeslot'
    timeID = db.Column(db.Integer, primary_key=True)
    timeDescription = db.Column(db.String(20), nullable=False)

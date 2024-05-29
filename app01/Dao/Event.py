from __init__ import db


class Event(db.Model):
    __tablename__ = 'tempevent'
    eventID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    eventName = db.Column(db.String(45), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    reservationUserId = db.Column(db.Integer, nullable=False)
    eventTypeID = db.Column(db.Integer, nullable=False)
    numberOfPeople = db.Column(db.Integer, nullable=False)
    preferredLocation = db.Column(db.String(100), nullable=False)
    arrangedLocation = db.Column(db.String(100), nullable=True)
    requireApproval = db.Column('requireApproval', db.Boolean, default=False)
    time = db.Column(db.String(100), nullable=False)


    def __repr__(self):
        return f"<Event {self.eventName}>"

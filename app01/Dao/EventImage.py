from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class EventImage(db.Model):
    __tablename__ = 'EventImage'
    
    id = db.Column(db.Integer, primary_key=True)
    eventID = db.Column(db.Integer, db.ForeignKey('events.eventID'), nullable=False)
    image_path = db.Column(db.String, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f"<EventImage {self.id}>"
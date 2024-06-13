from __init__ import db

class Comment(db.Model):
    __tablename__ = 'Comment'
    CommentID = db.Column('ID', db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column('UserID', db.Integer, db.ForeignKey('User.UserID'), nullable=False)
    Username = db.Column('Username', db.String(50), nullable=False)
    Answer = db.Column('Answer', db.Text, nullable=False)
    AnsTime = db.Column('AnsTime', db.TIMESTAMP, default=db.func.current_timestamp())
    EventID = db.Column('EventID', db.Integer, db.ForeignKey('event.eventID'), nullable=False)
    user = db.relationship('User', backref=db.backref('comments', lazy=True))
    AnswerTo = db.Column('AnswerTo', db.Integer, nullable=True)

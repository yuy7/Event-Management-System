from __init__ import db


class InvitedList(db.Model):
    __tablename__ = 'invitedlist'

    listID = db.Column(db.Integer, primary_key=True)
    inviteType = db.Column(db.Integer, nullable=False)
    eventID = db.Column(db.Integer, nullable=False)
    invitedID = db.Column(db.Integer, nullable=False)



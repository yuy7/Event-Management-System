from sqlalchemy.orm import backref

from __init__ import db


class Budget(db.Model):
    __tablename__ = 'Budget'
    budgetID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    eventID = db.Column(db.Integer, db.ForeignKey('event.eventID'), nullable=True)
    # userID = db.Column(db.Integer, db.ForeignKey('User.UserID'), nullable=True)
    initialBudget = db.Column(db.Numeric(10, 2))
    actualCost = db.Column(db.Numeric(10, 2))
    createdAt = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updatedAt = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    event = db.relationship('Event', uselist=False, backref=backref('budget', uselist=False))


class BudgetApp(db.Model):
    __tablename__ = 'BudgetApp'
    BudgetAppID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userID = db.Column(db.Integer, db.ForeignKey('User.UserID'), nullable=True)
    eventID = db.Column(db.Integer, db.ForeignKey('event.eventID'), nullable=True)
    cost = db.Column(db.Numeric(10, 2))
    status = db.Column(db.String(10))

    event = db.relationship('Event', uselist=False, backref=backref('budgetApps', uselist=True))
    user = db.relationship('User', uselist=False, backref=backref('budgetApps', uselist=True))

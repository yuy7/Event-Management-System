from app01 import db


class Budget(db.Model):
    __tablename__ = 'Budget'
    budgetID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # eventID = db.Column(db.Integer, db.ForeignKey('Event.eventID'), nullable=True)
    # userID = db.Column(db.Integer, db.ForeignKey('User.UserID'), nullable=True)
    initialBudget = db.Column(db.Numeric(10, 2))
    actualCost = db.Column(db.Numeric(10, 2))
    createdAt = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updatedAt = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

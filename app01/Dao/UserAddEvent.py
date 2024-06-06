from __init__ import db

class UserAddEvent(db.Model):
    __tablename__ = 'user_add_event'
    userID = db.Column(db.Integer, db.ForeignKey('User.UserID'), primary_key=True)
    eventID = db.Column(db.Integer, db.ForeignKey('event.eventID',primary_key=True))
    state = db.Column(db.Integer, default=0)  # 默认值为0表示“审批中”, 1表示“已加入”, 2表示“被拒绝”

from __init__ import db
from datetime import datetime

class Application(db.Model):
    __tablename__ = 'Application'  # 明确设置表名
    applicationID = db.Column('id', db.Integer, primary_key=True)  # 主键
    eventID = db.Column('eventId', db.Integer, db.ForeignKey('Event.eventID'), nullable=False)  # 外键关联到Event表
    userID = db.Column('userId', db.Integer, db.ForeignKey('User.UserID'), nullable=False)  # 假设用户表的主键为userID
    status = db.Column('status', db.String(10), default='pending', nullable=False)  # 申请状态
    applyDate = db.Column('applyDate', db.TIMESTAMP)  # 申请时间，使用 TIMESTAMP

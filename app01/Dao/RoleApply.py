from __init__ import db

class RoleApply(db.Model):
    __tablename__ = 'RoleApply'
    roleApplyID = db.Column('roleApplyID', db.Integer, primary_key=True)
    userID = db.Column('userID', db.Integer,db.ForeignKey('User.UserID'))
    roleID = db.Column('roleID', db.Integer,db.ForeignKey('Role.roleID'))
    roleState = db.Column('roleState', db.Integer, default=0)
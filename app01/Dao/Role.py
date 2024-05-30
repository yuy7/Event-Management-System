from __init__ import db


class Role(db.Model):
    __tablename__ = 'Role'
    roleID = db.Column('roleID', db.Integer, primary_key=True)
    roleName = db.Column('roleName', db.String(45))

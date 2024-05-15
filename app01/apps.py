import os

import sqlalchemy as sqlalchemy
from flask import Flask, jsonify, request
from flask_cors import CORS


from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from Model.Login import user_login
from __init__ import init_db

from datetime import datetime
app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)
# username: root, password: root
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/event?charset=utf8'
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'User'
    UserID = db.Column('UserID', db.Integer, primary_key=True)
    Username = db.Column('Username', db.String(50))
    Password = db.Column('Password', db.String(100))
    Email = db.Column('Email', db.String(100))
    PhoneNumber = db.Column('PhoneNumber', db.String(20))
    Role = db.Column('Role', db.String(20))
    VerificationCode = db.Column('VerificationCode', db.String(20))
    RegistrationTime = db.Column('RegistrationTime', db.TIMESTAMP, default=db.func.current_timestamp())
    LastLoginTime = db.Column('LastLoginTime', db.TIMESTAMP)
    AccountStatus = db.Column('AccountStatus', db.String(20))

# @app.route("/login", methods=["POST"])
# def login_router():
#     return user_login(request)

class Event(db.Model):
    __tablename__ = 'Event'
    eventID = db.Column('eventID', db.Integer, primary_key=True)
    eventName = db.Column('eventName', db.String(45))
    eventStartDate = db.Column('eventStartDate', db.TIMESTAMP)
    eventEndDate = db.Column('eventEndDate', db.TIMESTAMP)
    eventLocation = db.Column('eventLocation', db.String(45))

@app.route("/events", methods=["GET"])
def get_events():
    events = Event.query.all()
    return jsonify([{
        'eventID': event.eventID,
        'eventName': event.eventName,
        'eventEndDate': event.eventEndDate.isoformat().replace('T', ' ').replace("-","."),  
        'eventStartDate': event.eventStartDate.isoformat().replace('T', ' ').replace("-","."),
        'eventLocation': event.eventLocation
    } for event in events])

@app.route("/login", methods=["POST"])
def user_login():
    """
    用户登录
    :return:
    """
    data = request.get_json()
    phoneNumber = data.get("phoneNumber")
    password = data.get("password")

    # 查询数据库
    user = User.query.filter_by(PhoneNumber=phoneNumber).first()

    # 若用户存在且密码正确，返回成功的响应
    if user and user.Password == password:
        return jsonify({
            "status": "Success"
        })

    # 否则返回错误信息
    else:
        return jsonify({
            "status": "False"
        })

@app.route("/eventCreate", methods=["POST"])
def EventCreate():
    data = request.get_json()
    eventName = data.get("name")
    eventStartDate = data.get("startDate")
    eventEndDate = data.get("endDate")
    eventLocation = data.get("location")
   
    # 创建新活动并保存到数据库
    newEvent = Event(eventName=eventName, eventStartDate=eventStartDate,eventEndDate=eventEndDate,eventLocation=eventLocation)
    db.session.add(newEvent)
    db.session.commit()
    return jsonify({
        "status": "Success",
        "message": "创建成功"
    })

if __name__ == "__main__":
    app.run(debug=True)

    
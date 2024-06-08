from flask import Flask, jsonify, request
from Dao.Event import Event
from Dao.EventDetail import EventDetail
from Dao.UserEvent import UserEvent
from Dao.User import User
from __init__ import db
from Tool.Mappings import time_mapping
app = Flask(__name__)

def get_event():
    data = request.get_json()

    if not data:
        return jsonify({
            "status": "Failure",
            "message": "No input data provided"
        }), 400

    event_id = data.get("eventID")
    
    if not event_id:
        return jsonify({
            "status": "Failure",
            "message": "Event ID is required"
        }), 400

    # 查询数据库中是否存在对应的event
    event = Event.query.filter_by(eventID=event_id).first()
    
    if not event:
        return jsonify({
            "status": "Failure",
            "message": "Event not found"
        }), 404

    # 查询活动详情
    event_detail = EventDetail.query.filter_by(eventID=event_id).first()
    time_slot = time_mapping.get(event.time, "未知时间段")
    
    # 获取活动参与者的用户名
    participants = UserEvent.query.filter_by(eventID=event_id).all()
    participant_usernames = []
    for participant in participants:
        user = User.query.filter_by(UserID=participant.userID).first()
        if user:
            participant_usernames.append(user.Username)
    # 返回活动的相关信息
    event_info = {
        "eventID": event.eventID,
        "eventName": event.eventName,
        "date": event.date,
        "reservationUserId": event.reservationUserId,
        "eventTypeID": event.eventTypeID,
        "numberOfPeople": event.numberOfPeople,
        "preferredLocation": event.preferredLocation,
        "arrangedLocation": event.arrangedLocation,
        "requireApproval": event.requireApproval,
        "time": time_slot,
        "description": event_detail.description if event_detail else None,
        "notification": event_detail.notification if event_detail else None,
        "participants": participant_usernames
    }

    return jsonify({
        "status": "Success",
        "event": event_info
    }), 200

def getResult():
    return '.....'


def submitFeedback():
    data = request.get_json()
    event_id = data.get("eventid")
    user_id = data.get("userid")
    feedback = data.get("feedback")
    
    return 1
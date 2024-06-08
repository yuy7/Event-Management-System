from flask import Flask, jsonify, request
from Dao.Event import Event
from Dao.EventDetail import EventDetail
from Dao.EventFeedback import EventFeedback
from datetime import datetime
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
        "notification": event_detail.notification if event_detail else None
    }

    return jsonify({
        "status": "Success",
        "event": event_info
    }), 200

def getResult():
    return '.....'

def getUserRole():
    data = request.get_json()
    event_id = data.get("eventid")
    user_id = data.get("userid")
    event = Event.query.filter(Event.eventID==event_id, Event.reservationUserId==user_id).all()
    if len(event) > 0:
        return 'reservationUser'
    else: 
        return 'participant'

def getAllFeedback():
    data = request.get_json()
    event_id = data.get("eventid")
    feedback_query = EventFeedback.query.filter_by(eventID=event_id).all()
    # 转换查询结果为列表的字典形式
    feedbackList = [
        {
            'feedbackId': feedback.feedbackId,
            'userID': feedback.userID,
            'eventID': feedback.eventID,
            'feedback': feedback.feedback,
            'feedbackTime': feedback.feedbackTime.strftime("%Y-%m-%d %H:%M:%S") if feedback.feedbackTime else None
        } for feedback in feedback_query
    ]

    # 使用jsonify返回JSON数据
    return jsonify(feedbackList), 200

def submitFeedback():
    data = request.get_json()
    event_id = data.get("eventid")
    user_id = data.get("userid")
    feedback = data.get("feedback")
    feedback_time = datetime.now()

    # 创建EventFeedback对象，加入时间戳
    feedback_entry = EventFeedback(userID=user_id, eventID=event_id, feedback=feedback, feedbackTime=feedback_time)

    # 将对象添加到session并提交到数据库
    db.session.add(feedback_entry)
    db.session.commit()

    return jsonify({"success": True, "message": "Feedback submitted successfully"}), 200
    
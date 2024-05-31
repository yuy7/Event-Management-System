from flask import Flask, jsonify, request
from Dao.Event import Event
from Dao.EventDetail import EventDetail
from __init__ import db

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
        "time": event.time,
        "description": event_detail.description if event_detail else None,
        "notification": event_detail.notification if event_detail else None
    }

    return jsonify({
        "status": "Success",
        "event": event_info
    }), 200
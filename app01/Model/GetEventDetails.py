from flask import jsonify, request, session
from Dao.TempEvent import Event


def get_events():
    data = request.get_json()
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
        "time": event.time
    }

    return jsonify({
        "status": "Success",
        "event": event_info
    })

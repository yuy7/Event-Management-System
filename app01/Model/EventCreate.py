from flask import jsonify, request, session
from Dao.Event import Event
from __init__ import db

def EventCreate():
    # user_id = session.get("userID")
    user_id = 251101164
    data = request.get_json()
    eventName = data.get("name")
    date = data.get("date")
    eventTypeID = data.get("eventTypeID")
    numberOfPeople = data.get("numberOfPeople")
    preferredLocation = data.get("preferredLocation")
    requireApproval = data.get("requireApproval")
    time = data.get("time")
    
    
    # 创建新活动并保存到数据库
    newEvent = Event(
        eventName=eventName,
        date=date,
        reservationUserId=user_id,
        eventTypeID=eventTypeID,
        numberOfPeople=numberOfPeople,
        preferredLocation=preferredLocation,
        requireApproval=requireApproval,
        time=time
    )
    db.session.add(newEvent)
    db.session.commit()
    return jsonify({
        "status": "Success",
        "message": "创建成功"
    })


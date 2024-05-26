from flask import jsonify, request, session
from Dao.Event import Event
from __init__ import db

def EventCreate():
    data = request.get_json()
    eventName = data.get("name")
    eventStartDate = data.get("startDate")
    eventEndDate = data.get("endDate")
    eventLocation = data.get("location")
    requireApproval = data.get("requireApproval", False)  # 默认为False，如果请求中没有提供，则使用False

    user_id = session.get("userID")
    
    # 创建新活动并保存到数据库
    newEvent = Event(eventName=eventName, eventStartDate=eventStartDate, eventEndDate=eventEndDate, eventLocation=eventLocation, requireApproval=requireApproval, reservationUserId=user_id)
    db.session.add(newEvent)
    db.session.commit()
    return jsonify({
        "status": "Success",
        "message": "创建成功"
    })


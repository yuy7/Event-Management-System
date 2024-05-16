from flask import jsonify, request
from Dao.Event import Event
from __init__ import db

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
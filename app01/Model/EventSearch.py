from flask import request, jsonify
from __init__ import db
from Dao.Event import Event
from Dao.TimeSlot import TimeSlot
def search_events():
    search_query = request.args.get('searchQuery')

    # 在数据库中进行模糊查询，查找包含搜索关键词的事件
    events = db.session.query(Event, TimeSlot).join(TimeSlot, Event.time == TimeSlot.timeID).filter(Event.eventName.ilike(f"%{search_query}%")).all()

    # 将查询结果转换为字典列表
    events_list = []
    for event in events:
        events_list.append({
        'eventID': event.Event.eventID,
        'eventName': event.Event.eventName,
        'date': event.Event.date,
        'reservationUserId': event.Event.reservationUserId,
        'eventTypeID': event.Event.eventTypeID,
        'numberOfPeople': event.Event.numberOfPeople,
        'preferredLocation': event.Event.preferredLocation,
        'arrangedLocation': event.Event.arrangedLocation if event.Event.arrangedLocation else "Not arranged",
        'requireApproval': event.Event.requireApproval,
        'time': event.TimeSlot.timeDescription
        })

    return jsonify(events_list)

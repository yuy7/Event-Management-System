from flask import request, jsonify
from __init__ import db
from Dao.Event import Event
from Dao.UserEvent import UserEvent
from Dao.UserAddEvent import UserAddEvent
from Dao.TimeSlot import TimeSlot
from datetime import datetime

def get_start_and_end_timestamp(date_str, time_range_str):
    # 从时间范围中分解出开始时间和结束时间
    start_time_str, end_time_str = time_range_str.split('-')
    print(start_time_str, end_time_str)
    
    # 组合日期和开始时间为一个完整的日期时间字符串
    start_datetime_str = f"{date_str} {start_time_str}"
    end_datetime_str = f"{date_str} {end_time_str}"
    print(start_datetime_str, end_datetime_str)
    # 定义日期时间字符串的格式
    datetime_format = '%Y-%m-%d %H:%M'
    
    # 解析开始和结束的日期时间字符串为datetime对象
    start_datetime = datetime.strptime(start_datetime_str, datetime_format)
    end_datetime = datetime.strptime(end_datetime_str, datetime_format)
    
    return start_datetime, end_datetime

def isAddEvent(event_id, user_id):
    event = Event.query.filter(Event.eventID==event_id, Event.reservationUserId==user_id).all()
    if len(event) > 0:
        return True
    event = UserEvent.query.filter(UserEvent.userID==user_id, UserEvent.eventID==event_id).all()
    if len(event) > 0:
        return True
    event = UserAddEvent.query.filter(UserAddEvent.userID==user_id, UserAddEvent.eventID==event_id, UserAddEvent.state==1).all()
    if len(event) > 0:
        return True
    return False


def getLabel(event_id, user_id, date, time):
    start_time, end_time = get_start_and_end_timestamp(date, time)
    now = datetime.now()
    if end_time < now: 
        return '已结束'
    elif start_time <= now and end_time >= now:
        return '进行中'
    elif isAddEvent(int(event_id), int(user_id)):
        return '已加入'
    else: 
        return '加入'

def search_events():
    userID = request.args.get("userid")
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
        'time': event.TimeSlot.timeDescription,
        'label': getLabel(event.Event.eventID, userID, event.Event.date, event.TimeSlot.timeDescription)
        })

    return jsonify(events_list)

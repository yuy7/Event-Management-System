from Dao.Event import Event
from Dao.UserAddEvent import UserAddEvent
from Dao.TimeSlot import TimeSlot
from Dao.UserAddEvent import UserAddEvent
from datetime import datetime
from __init__ import db

def getUserAllEventByUserID(userID):
    today_str = datetime.now().strftime('%Y-%m-%d')
    own_events = db.session.query(Event, TimeSlot).join(TimeSlot, Event.time == TimeSlot.timeID).filter(
            Event.reservationUserId == userID, 
            Event.date >= today_str).all()
        
    # 查询 Event 表中 reservationUserId 等于当前 userID 的事件信息
    participated_events_1 = db.session.query(Event, TimeSlot)\
                           .join(TimeSlot, Event.time == TimeSlot.timeID)\
                           .filter(Event.reservationUserId == userID)\
                           .filter(Event.date >= today_str)\
                           .all()
    

    # 查询 UserAddEvent 表中 userID 对应的 eventID 的事件信息
    participated_events_2 = db.session.query(Event, TimeSlot, UserAddEvent)\
                                    .join(TimeSlot, Event.time == TimeSlot.timeID)\
                                    .join(UserAddEvent, UserAddEvent.eventID == Event.eventID)\
                                    .filter(UserAddEvent.userID == userID)\
                                    .filter(Event.date >= today_str)\
                                    .filter(UserAddEvent.state == 1)\
                                    .all()
    

    # 合并查询结果
    event_list = []
    
    # 处理 own_events
    for event in own_events:
        event_list.append({
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
            'state': 0  # 表示这个事件是用户自己预订的
        })
    
    # 处理 participated_events
    for event in participated_events_1:
        event_list.append({
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
            'state': 1  # 表示这个事件是用户参与的
        })

    for event in participated_events_2:
        event_list.append({
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
            'state': 1  # 表示这个事件是用户参与的
        })
    return event_list
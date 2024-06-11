from datetime import datetime
from Dao.UserEvent import UserEvent
from Dao.UserAddEvent import UserAddEvent
from  Dao.Event import Event
from Dao.User import User
from flask import session,request
from __init__ import db
from Dao.TimeSlot import TimeSlot
from Tool.Mappings import mapping_add_state
from Tool.Mappings import event_type_mapping

def getHistoryEvents():
    # data = request.get_json()
    # userID = data.get("userid")
    # userID = session.get("userid")  # 从session中获取userID
    userID = request.args.get("userid")
    print(userID)
    today_str = datetime.now().strftime('%Y-%m-%d')

    # 查询用户过去参加过的活动
    approved_event_ids = db.session.query(UserAddEvent.eventID).join(
        Event, UserAddEvent.eventID == Event.eventID
    ).filter(
        UserAddEvent.userID == userID,
        UserAddEvent.state == 1,
        Event.date < today_str
    ).all()
    print(approved_event_ids)

    # Query for non-approval required event IDs
    non_approval_event_ids = db.session.query(UserEvent.eventID).join(
        Event, UserEvent.eventID == Event.eventID
    ).filter(
        UserEvent.userID == userID,
        Event.date < today_str
    ).all()
    print(non_approval_event_ids)
    # Create a combined list of all unique eventIDs (approved and non-approval required)
    joined_event_ids = {event_id for (event_id,) in approved_event_ids + non_approval_event_ids}

    # Query the Event table to retrieve Event objects for the combined list of eventIDs
    attended_events = Event.query.filter(Event.eventID.in_(joined_event_ids)).all()
    print(attended_events)
    # 查询用户过去预约过的活动
    reserved_events = Event.query.filter(
            Event.reservationUserId == userID, 
            Event.date < today_str).all()
    print(reserved_events)
    # 合并两个列表，并去重（假定一个事件不可能同时在两个列表中）
    all_history_events = attended_events+reserved_events
    events_json = [{
        'eventID': event.eventID,
        'eventName': event.eventName,
        'date': event.date,
        'reservationUserId': User.query.filter_by(UserID=event.reservationUserId).first().Username,
        'eventTypeID': event_type_mapping[event.eventTypeID],
        'numberOfPeople': event.numberOfPeople,
        'preferredLocation': event.preferredLocation,
        'arrangedLocation': event.arrangedLocation if event.arrangedLocation else "Not arranged",
        'time': TimeSlot.query.filter_by(timeID=event.time).first().timeDescription if TimeSlot.query.filter_by(timeID=event.time).first() else "Time not found"  # 从TimeSlot关系中访问timeDescription，确保有结果才访问属性
    } for event in all_history_events]
    print(events_json)
    return events_json
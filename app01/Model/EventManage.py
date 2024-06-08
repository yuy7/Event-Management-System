from flask import jsonify, request, session
from Dao.Event import Event
from Dao.UserEvent import UserEvent
from Dao.UserAddEvent import UserAddEvent
from Dao.TimeSlot import TimeSlot
from Dao.UserAddEvent import UserAddEvent
from Dao.User import User
from __init__ import db
from Tool.Mappings import mapping_add_state
from datetime import datetime
from Tool.GetUserAllEvent import getUserAllEventByUserID


def get_events():
    # userID = session.get("userid")
    userID = request.args.get("userid")
    if not userID:
        return jsonify({'error': 'User not logged in'}), 401  # 如果没有userID，返回错误信息
    today_str = datetime.now().strftime('%Y-%m-%d')
    
    # 修改查询，增加一个过滤条件，使用Event.date >= today_str来筛选日期为今天或未来的事件
    events = db.session.query(Event, TimeSlot).join(TimeSlot, Event.time == TimeSlot.timeID).filter(Event.date >= today_str).all()
    return jsonify([{
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
    } for event in events])


def getUserEvent():
    userID = session.get("userID")
    # userID = 251101164
    today_str = datetime.now().strftime('%Y-%m-%d')
    eventList = db.session.query(Event, TimeSlot).join(TimeSlot, Event.time == TimeSlot.timeID).filter(
            Event.reservationUserId == userID, 
            Event.date >= today_str).all()
    return jsonify([{
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
    } for event in eventList])

def getUserAddEvent():
    userID = request.args.get("userid")
    # userID = session.get("userID")
    # Query for approved event IDs
    today_str = datetime.now().strftime('%Y-%m-%d')
    approved_event_ids = db.session.query(UserAddEvent.eventID).join(
        Event, UserAddEvent.eventID == Event.eventID
    ).filter(
        UserAddEvent.userID == userID,
        Event.date >= today_str
    ).all()


    # Query for non-approval required event IDs
    non_approval_event_ids = db.session.query(UserEvent.eventID).join(
        Event, UserEvent.eventID == Event.eventID
    ).filter(
        UserEvent.userID == userID,
        Event.date >= today_str
    ).all()

    # Create a combined list of all unique eventIDs (approved and non-approval required)
    joined_event_ids = {event_id for (event_id,) in approved_event_ids + non_approval_event_ids}

    # Query the Event table to retrieve Event objects for the combined list of eventIDs
    eventList = Event.query.filter(Event.eventID.in_(joined_event_ids)).all()
    # 构建字典列表
    events_json = [{
        'eventID': event.eventID,
        'eventName': event.eventName,
        'date': event.date,
        'reservationUserId': event.reservationUserId,
        'eventTypeID': event.eventTypeID,
        'numberOfPeople': event.numberOfPeople,
        'preferredLocation': event.preferredLocation,
        'arrangedLocation': event.arrangedLocation if event.arrangedLocation else "Not arranged",
        'requireApproval': event.requireApproval,
        'state': mapping_add_state[UserAddEvent.query.filter(UserAddEvent.userID == userID, UserAddEvent.eventID == event.eventID).first().state 
        if UserAddEvent.query.filter(UserAddEvent.userID == userID, UserAddEvent.eventID == event.eventID).first() is not None 
        else 1],  # 如果没有找到记录，默认状态设为1（已批准）
        'time': TimeSlot.query.filter_by(timeID=event.time).first().timeDescription if TimeSlot.query.filter_by(timeID=event.time).first() else "Time not found"  # 从TimeSlot关系中访问timeDescription，确保有结果才访问属性
    } for event in eventList]
    print(events_json)
    return events_json

def deleteEvent():
    eventID = request.json.get('eventID')
    # eventID = request.args.get("eventID")
    event = Event.query.filter_by(eventID=eventID).first()
    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Event deleted'}), 200

# 得到用户加入和创建的所有活动
def getUserAllEvent():
    # userID = session.get("userID")
    # userID = 251101164
    userID = request.args.get("userid")

    event_list = getUserAllEventByUserID(userID)
    return jsonify(event_list)
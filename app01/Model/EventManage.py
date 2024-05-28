from flask import jsonify, request, session
from Dao.Event import Event
from Dao.User import User
from Dao.TimeSlot import TimeSlot
from __init__ import db


def get_events():
    userID = session.get("userID")
    if not userID:
        return jsonify({'error': 'User not logged in'}), 401  # 如果没有userID，返回错误信息
    events = Event.query.all()
    print(events)
    return jsonify([{
        'eventID': event.eventID,
        'eventName': event.eventName,
        'date': event.date,
        'reservationUserId': event.reservationUserId,
        'eventTypeID': event.eventTypeID,
        'numberOfPeople': event.numberOfPeople,
        'preferredLocation': event.preferredLocation,
        'arrangedLocation': event.arrangedLocation if event.arrangedLocation else "Not arranged",
        'requireApproval': event.requireApproval,
        'time': event.time # 使用映射转换时间
    } for event in events])


def getUserEvent():
    userID = session.get("userID")
    eventList = db.session.query(Event, TimeSlot).join(TimeSlot, Event.time == TimeSlot.timeID).filter(Event.reservationUserId == userID).all()
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

def deleteEvent():
    eventID = request.json.get('eventID')
    event = Event.query.filter_by(eventID=eventID).first()
    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Event deleted'}), 200
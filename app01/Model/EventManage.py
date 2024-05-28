from flask import jsonify, request, session
from Dao.Event import Event
from Dao.User import User



def get_events():
    userID = session.get("userID")
    # if not userID:
    #     return jsonify({'error': 'User not logged in'}), 401  # 如果没有userID，返回错误信息
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

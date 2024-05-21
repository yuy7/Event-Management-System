from flask import jsonify, request
from Dao.Event import Event
from Dao.User import User

def get_events():
    currentUserId = request.args.get('userid', '')
    print(currentUserId)
    events = Event.query.all()
    return jsonify([{
        'eventID': event.eventID,
        'eventName': event.eventName,
        'eventEndDate': event.eventEndDate.isoformat().replace('T', ' ').replace("-","."),  
        'eventStartDate': event.eventStartDate.isoformat().replace('T', ' ').replace("-","."),
        'eventLocation': event.eventLocation
    } for event in events])
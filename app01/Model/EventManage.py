from flask import jsonify, request, session
from Dao.Event import Event
from Dao.User import User

def get_events():
    events = Event.query.all()
    return jsonify([{
        'eventID': event.eventID,
        'eventName': event.eventName,
        'eventEndDate': event.eventEndDate.isoformat().replace('T', ' ').replace("-","."),  
        'eventStartDate': event.eventStartDate.isoformat().replace('T', ' ').replace("-","."),
        'eventLocation': event.eventLocation,
        'creatorid': event.creator_id
    } for event in events])
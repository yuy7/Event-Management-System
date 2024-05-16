from flask import jsonify
from Dao.Event import Event

def get_events():
    events = Event.query.all()
    return jsonify([{
        'eventID': event.eventID,
        'eventName': event.eventName,
        'eventEndDate': event.eventEndDate.isoformat().replace('T', ' ').replace("-","."),  
        'eventStartDate': event.eventStartDate.isoformat().replace('T', ' ').replace("-","."),
        'eventLocation': event.eventLocation
    } for event in events])
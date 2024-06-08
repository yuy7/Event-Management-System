from flask import Flask, request, jsonify
from __init__ import db
from Dao.EventDetail import EventDetail
from Dao.Event import Event

def update_notification():
    data = request.get_json()
    event_id = data.get('eventID')
    notification = data.get('notification')
    user_id = data.get('userID')

    # Check for missing parameters
    if not event_id or not notification or not user_id:
        return jsonify({"message": "Missing required parameters"}), 400

    event = Event.query.get(event_id)
    if not event:
        return jsonify({"message": "Event not found"}), 404

    # Convert user_id and reservationUserId to integer for comparison
    user_id = int(user_id)
    reservation_user_id = int(event.reservationUserId)

    # Check if the user is authorized to publish the notification
    if reservation_user_id != user_id:
        print(reservation_user_id, user_id)
        return jsonify({'message': 'You are not authorized to publish a notification for this event.'}), 403

    event_detail = EventDetail.query.filter_by(eventID=event_id).first()
    if not event_detail:
        return jsonify({"message": "Event details not found"}), 404

    # Update the notification
    event_detail.notification = notification
    db.session.commit()
    return jsonify({"message": "Notification updated successfully"}), 200




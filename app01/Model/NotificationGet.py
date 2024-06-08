from flask import jsonify, request
from __init__ import db
from Dao.Notification import Notification
from Dao.UserAddEvent import UserAddEvent
from Dao.UserEvent import UserEvent

def getSystemNotifications():
    user_id = request.args.get("userid")
    notifications = Notification.query.filter(
        Notification.recipient_id == user_id, 
        Notification.type == 1
    ).order_by(Notification.timestamp.desc()).all()

    unread_notifications = [notif for notif in notifications if not notif.read]
    for notification in unread_notifications:
        notification.read = True
    
    if unread_notifications:
        db.session.commit()

    notifications_list = [{
        'id': notification.id,
        'sender_id': notification.sender_id,
        'event_id': notification.event_id,
        'message': notification.message,
        'read': notification.read,
        'type': notification.type,
        'timestamp': notification.timestamp.strftime('%Y-%m-%d %H:%M:%S')

    } for notification in notifications]
    
    return jsonify(notifications_list)


def getApprovalNotifications():
    user_id = request.args.get("userid")
    notifications = Notification.query.filter(
        Notification.recipient_id == user_id, 
        Notification.type == 2
    ).order_by(Notification.timestamp.desc()).all()

    unread_notifications = [notif for notif in notifications if not notif.read]
    for notification in unread_notifications:
        notification.read = True
    
    if unread_notifications:
        db.session.commit()

    notifications_list = [{
        'id': notification.id,
        'sender_id': notification.sender_id,
        'event_id': notification.event_id,
        'message': notification.message,
        'read': notification.read,
        'type': notification.type,
        'timestamp': notification.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    } for notification in notifications]
    
    return jsonify(notifications_list)


def acceptEventApply():
    eventApplyID = request.json.get("notificationID")
    eventApply = Notification.query.filter_by(id=eventApplyID).first()
    
    if not eventApply:
        return jsonify({"status": "Error", "message": "Notification not found"}), 404

    try:
        userAddEvent = UserAddEvent.query.filter(
            UserAddEvent.userID == eventApply.sender_id, 
            UserAddEvent.eventID == eventApply.event_id
        ).first()
        if userAddEvent:
            userAddEvent.state = 1
        
        eventApply.read = True
        
        # 插入到 UserEvent 表中
        userEvent = UserEvent(userID=eventApply.sender_id, eventID=eventApply.event_id)
        db.session.add(userEvent)

        db.session.commit()
        return jsonify({"status": "Success"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "Error", "message": str(e)}), 500


def refuseEventApply():
    eventApplyID = request.json.get("notificationID")
    eventApply = Notification.query.filter_by(id=eventApplyID).first()

    if not eventApply:
        return jsonify({"status": "Error", "message": "Notification not found"}), 404

    try:
        userAddEvent = UserAddEvent.query.filter(
            UserAddEvent.userID == eventApply.sender_id, 
            UserAddEvent.eventID == eventApply.event_id
        ).first()
        if userAddEvent:
            userAddEvent.state = 2
        
        eventApply.read = True

        db.session.commit()
        return jsonify({"status": "Success"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "Error", "message": str(e)}), 500

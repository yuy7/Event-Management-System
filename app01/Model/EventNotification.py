from flask import Flask, request, jsonify
from __init__ import db
from Dao.EventDetail import EventDetail
from Dao.Event import Event

def getNotificationTemplate():
    event_id = request.args.get("eventid")
    # 从数据库中获取指定ID的活动信息
    event = Event.query.filter_by(eventID = event_id).first()

    if event is None:
        return "指定的活动不存在。"

    # 准备模板，并填充活动信息
    template = (
        f"{event.date}，我们将在{event.arrangedLocation or event.preferredLocation}举行{event.eventName}，"
        f"大家不要忘记来参加！"
    )

    return template


def saveNotification():
    # 从请求中获取 notification 和 event_id
    data = request.get_json()
    notification = data.get("notification")
    event_id = data.get("eventid")
    print(event_id)
    print(notification)
    # 检查是否提供了必要的信息
    if not notification or not event_id:
        return jsonify({'error': 'Missing result or event_id'}), 400

    # 查找 event detail 对象
    event_detail = db.session.query(EventDetail).filter(EventDetail.eventID == event_id).first()

    # 如果该 event detail 不存在，则创建一个新的
    if not event_detail:
        event_detail = EventDetail(eventID=event_id, notification=notification)
        db.session.add(event_detail)
    else:
        # 更新 result 属性
        event_detail.notification = notification

    # 提交更改到数据库
    db.session.commit()

    return jsonify({'message': 'Notification saved successfully'}), 200

def updateNotification():
    data = request.get_json()
    event_id = data.get('eventID')
    notification = data.get('notification')
    user_id = data.get('userID')
    print(event_id)
    print(notification)
    print(user_id)
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

def getNotification():
    event_id = request.args.get("eventid")

    # 检查是否提供了必要的 event_id
    if not event_id:
        return jsonify({'error': 'Missing event_id'}), 400

    # 查找 event detail 对象
    event_detail = db.session.query(EventDetail).filter(EventDetail.eventID == event_id).first()

    if not event_detail or not event_detail.notification:
        return ''
    else:
        return event_detail.notification


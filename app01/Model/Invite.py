from flask import Flask, jsonify, request
from __init__ import db
from datetime import datetime
from Dao.Event import Event
from Dao.User import User
from Dao.Class import Class
from Dao.InvitedList import InvitedList
from Dao.UserEvent import UserEvent
from Dao.UserAddEvent import UserAddEvent
from Dao.Notification import Notification

def get_invite_users():
    event_id = request.args.get('eventid')
    if not event_id:
        return jsonify({'status': 'Error', 'message': 'Event ID is required'}), 400

    # 获取预定用户的 ID
    event = Event.query.filter_by(eventID=event_id).first()
    if not event:
        return jsonify({'status': 'Error', 'message': 'Event not found'}), 404

    reservation_user_id = event.reservationUserId

    # 获取与事件相关的用户 ID 列表
    user_event_ids = set(user_event.userID for user_event in UserEvent.query.filter_by(eventID=event_id).all())
    user_add_event_ids = set(user_add_event.userID for user_add_event in UserAddEvent.query.filter(UserAddEvent.eventID==event_id, UserAddEvent.state==1).all())

    # 来自所有相关表的用户 ID
    exclude_user_ids = user_event_ids | user_add_event_ids 
    exclude_user_ids.add(reservation_user_id)
    exclude_user_ids.add(10086)

    # 获取所有用户
    users = User.query.all()
    filtered_users = [
        {
            'userID': user.UserID,
            'userName': user.Username,
            'email': user.Email,
            'phone': user.PhoneNumber,
            'role': user.Role,
        }
        for user in users if user.UserID not in exclude_user_ids
    ]

    return jsonify(filtered_users)

def invite():
    data = request.get_json()

    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    invite_type = data.get('inviteType')
    event_id = data.get('eventID')
    invited_id = data.get('invitedID')
    user_id = data.get('userID')

    if not invite_type or not event_id or not invited_id or not user_id:
        return jsonify({'message': 'Missing required fields'}), 400

    # 检查事件是否存在
    event = Event.query.filter_by(eventID=event_id).first()
    if not event:
        return jsonify({'message': 'Event not found'}), 404

    # 检查用户是否有权限邀请
    is_creator = (event.reservationUserId == int(user_id))
    print(event.reservationUserId)
    print(user_id)
    print(is_creator)
    is_participant = UserEvent.query.filter_by(userID=user_id, eventID=event_id).first()
    if not (is_creator or is_participant):
        return jsonify({'message': 'User not authorized to invite'}), 403

    # 检查被邀请对象是否存在
    if invite_type == 1:  # 个人
        invited = User.query.filter_by(UserID=invited_id).first()
        if not invited:
            return jsonify({'message': 'User not found'}), 404
    elif invite_type == 2:  # 班级
        invited = Class.query.filter_by(classID=invited_id).first()
        if not invited:
            return jsonify({'message': 'Class not found'}), 404
    else:
        return jsonify({'message': 'Invalid inviteType'}), 400

    # 创建邀请记录
    invite_record = InvitedList(inviteType=invite_type, eventID=event_id, invitedID=invited_id)
    db.session.add(invite_record)

    # 创建通知记录
    message = f'你被{User.query.filter_by(userID=user_id).first().Username}邀请加入 {event_id}'
    notification = Notification(
        recipient_id=invited_id,
        sender_id=user_id,
        event_id=event_id,
        message=message,
        read=False,
        timestamp=datetime.now(),
        type=4
    )
    db.session.add(notification)
    
    db.session.commit()

    return jsonify({'message': 'Invite sent successfully'}), 200

def getValidationNotifications():
    user_id = request.args.get("userid")
    notifications = Notification.query.filter(
        Notification.recipient_id == user_id, 
        Notification.type == 4  # type 4 表示邀请消息
    ).order_by(Notification.timestamp.desc()).all()

    unread_notifications = [notif for notif in notifications if not notif.read]
    for notification in unread_notifications:
        notification.read = True
    
    if unread_notifications:
        db.session.commit()

    notifications_list = [{
        'id': notification.id,
        'recipient_id': notification.recipient_id,
        'sender_id': notification.sender_id,
        'event_id': notification.event_id,
        'message': notification.message,
        'read': notification.read,
        'type': notification.type,
        'timestamp': notification.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    } for notification in notifications]
    
    return jsonify(notifications_list)

def acceptInvite():
    event_id = request.json.get('eventID')
    user_id = request.json.get('userID')

    invite = InvitedList.query.filter_by(eventID=event_id, invitedID=user_id).first()

    if not invite:
        return jsonify({'status': 'Error', 'message': 'Invite not found'}), 404

    try:
        # 添加用户到 UserEvent 表中
        user_event = UserEvent(userID=user_id, eventID=invite.eventID)
        db.session.add(user_event)

        # 删除邀请记录
        db.session.delete(invite)

        # 设置通知为已读
        notification = Notification.query.filter_by(event_id=invite.eventID, recipient_id=user_id).first()
        if notification:
            notification.read = True

        db.session.commit()
        return jsonify({'status': 'Success'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'Error', 'message': str(e)}), 500

def refuseInvite():
    event_id = request.json.get('eventID')
    user_id = request.json.get('userID')

    invite = InvitedList.query.filter_by(eventID=event_id, invitedID=user_id).first()

    if not invite:
        return jsonify({'status': 'Error', 'message': 'Invite not found'}), 404

    try:
        # 删除邀请记录
        db.session.delete(invite)

        # 设置通知为已读
        notification = Notification.query.filter_by(event_id=invite.eventID, recipient_id=user_id).first()
        if notification:
            notification.read = True

        db.session.commit()
        return jsonify({'status': 'Success'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'Error', 'message': str(e)}), 500

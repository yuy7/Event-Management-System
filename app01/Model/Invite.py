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
    user_add_event_ids = set(user_add_event.userID for user_add_event in
                             UserAddEvent.query.filter(UserAddEvent.eventID == event_id, UserAddEvent.state == 1).all())

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
    message = f'你被{User.query.filter_by(UserID=user_id).first().Username}邀请加入 {Event.query.filter_by(eventID=event_id).first().eventName}'
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


def force_invite():
    data = request.get_json()

    if not data:
        return jsonify({'message': '未提供输入数据'}), 400

    event_id = data.get('eventID')
    invited_ids = data.get('invitedIDs')  # 这里是一个列表，包含所有要邀请的用户ID
    user_id = data.get('userID')

    if not event_id or not invited_ids or not user_id:
        return jsonify({'message': '缺少必需字段'}), 400

    # 检查发起请求的用户是否具有权限
    requesting_user = User.query.filter_by(UserID=user_id).first()
    event = Event.query.filter_by(eventID=event_id).first()

    if not requesting_user or not event or str(event.reservationUserId) != str(user_id):
        return jsonify({'message': '用户无权强制邀请'}), 403

    # 检查事件是否存在
    if not event:
        return jsonify({'message': '未找到活动'}), 404

    try:
        for invited_id in invited_ids:
            # 检查用户是否已经在活动中
            existing_user_event = UserEvent.query.filter_by(userID=invited_id, eventID=event_id).first()
            if not existing_user_event:
                # 添加用户到 UserEvent 表中
                user_event = UserEvent(userID=invited_id, eventID=event_id)
                db.session.add(user_event)
                # 创建通知记录
                message = f'你已被{User.query.filter_by(UserID=user_id).first().Username}强制邀请加入活动 {Event.query.filter_by(eventID=event_id).first().eventName}'
                notification = Notification(
                    recipient_id=invited_id,
                    sender_id=user_id,
                    event_id=event_id,
                    message=message,
                    read=False,
                    timestamp=datetime.now(),
                    type=1
                )
                db.session.add(notification)
        db.session.commit()
        return jsonify({'message': '用户强制邀请成功'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '发生错误: ' + str(e)}), 500


def get_available_users():
    event_id = request.args.get('eventid')

    if not event_id:
        return jsonify({'message': '缺少活动ID'}), 400

    # 获取所有还未加入活动的用户
    subquery = db.session.query(UserEvent.userID).filter(UserEvent.eventID == event_id).subquery()
    available_users = User.query.filter(User.UserID.notin_(subquery), User.Role != '0').all()

    user_list = [{'UserID': user.UserID, 'Username': user.Username} for user in available_users]

    return jsonify({'users': user_list}), 200


from Dao.Class import Class, ClassUser


def invite_class():
    # 从请求中获取 JSON 数据
    data = request.get_json()

    # 提取 eventID、classID 和 userID
    event_id = data.get('eventID')
    class_id = data.get('classID')
    user_id = data.get('userID')

    # 检查是否缺少必需字段
    if not event_id or not class_id or not user_id:
        return jsonify({'message': '缺少必需字段'}), 400

    try:
        # 获取班级中的所有用户
        class_users = ClassUser.query.filter_by(ClassID=class_id).all()
        if not class_users:
            return jsonify({'message': '未找到班级用户'}), 404

        # 遍历班级中的每个用户
        for class_user in class_users:
            invited_id = class_user.UserID
            # 检查用户是否已经在活动中
            existing_user_event = UserEvent.query.filter_by(userID=invited_id, eventID=event_id).first()
            if not existing_user_event:
                # 如果用户不在活动中，添加到 UserEvent 表中
                user_event = UserEvent(userID=invited_id, eventID=event_id)
                db.session.add(user_event)

                # 创建通知记录
                message = f'你被{User.query.filter_by(UserID=user_id).first().Username}邀请加入活动 {Event.query.filter_by(eventID=event_id).first().eventName}'
                notification = Notification(
                    recipient_id=invited_id,
                    sender_id=user_id,
                    event_id=event_id,
                    message=message,
                    read=False,
                    timestamp=datetime.now(),
                    type=1
                )
                db.session.add(notification)

        # 提交数据库事务
        db.session.commit()
        return jsonify({'message': '班级用户已成功邀请加入活动'}), 200

    except Exception as e:
        # 如果发生错误，回滚事务
        db.session.rollback()
        return jsonify({'message': '发生错误: ' + str(e)}), 500
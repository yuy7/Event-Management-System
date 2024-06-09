from flask import jsonify, request
from Dao.Event import Event
from Dao.Application import Application
from Dao.UserEvent import UserEvent  
from Dao.UserAddEvent import UserAddEvent
from Dao.TimeSlot import TimeSlot
from Dao.User import User  
from Dao.Notification import Notification  
from Tool.GetUserAllEvent import getUserAllEventByUserID
from __init__ import db

def notify_user(recipient_id, sender_id, event_id, message, type = 0):
    notification = Notification(
        recipient_id=recipient_id,
        sender_id=sender_id,
        event_id=event_id,
        message=message,
        type=type  # 传入通知类型
    )
    db.session.add(notification)
    db.session.commit()
    
def apply_event():
    data = request.get_json()
    user_id = data.get("userID")
    event_id = data.get("eventID")

    # 检查活动是否存在
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"status": "Error", "message": "活动不存在"}), 404
    

    time_slot = db.session.query(TimeSlot.timeDescription)\
                          .filter(TimeSlot.timeID == event.time)\
                          .first()
    
    time = time_slot.timeDescription if time_slot else None

    # 判断时间是否冲突
    event_list = getUserAllEventByUserID(user_id)
    for tmp_event in event_list:
        if tmp_event['date'] == event.date and tmp_event['time'] == time:
            return jsonify({
                'status': 'Error',
                'message': '时间冲突,冲突的活动名称为'+tmp_event['eventName']+'，请重新选择时间'
            }), 409

    # 获取活动创建者ID
    reservationUserId = event.reservationUserId
    if event.requireApproval:
        # 如果活动需要审批，则创建用户事件记录，并设置状态为0
        user_event = UserEvent(userID=user_id, eventID=event_id, state=0)
        db.session.add(user_event)
        db.session.commit()
        # 通知活动创建者有新的申请
        applicant = User.query.get(user_id)
        message = f"{applicant.Username} 申请加入您的活动 {event.eventName}"
        notify_user(reservationUserId, user_id, event_id, message, 2)  # 申请消息

        return jsonify({"status": "Success", "message": "申请已提交等待审批"}), 200
    else:
        # 如果活动不需要审批，则直接添加用户到活动，并设置状态为1
        user_event = UserEvent(userID=user_id, eventID=event_id)
        db.session.add(user_event)
        db.session.commit()

        # 通知活动创建者有新的成员加入
        new_member = User.query.get(user_id)
        message = f"{new_member.Username} 加入了您的活动 {event.eventName}"
        notify_user(reservationUserId, user_id, event_id, message, 1)  # 系统消息

        return jsonify({"status": "Success", "message": "成功加入活动"}), 200
    
def applyEventWithReason():
    data = request.get_json()
    user_id = data.get("userID")
    event_id = data.get("eventID")
    reason = data.get("reason")

    # 检查活动是否存在
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"status": "Error", "message": "活动不存在"}), 404

    # 获取活动创建者ID
    reservationUserId = event.reservationUserId
    if event.requireApproval:
        # 如果活动需要审批，则创建用户事件记录，并设置状态为0
        user_add_event = UserAddEvent(userID=user_id, eventID=event_id, state=0)
        db.session.add(user_add_event)
        db.session.commit()
        # 通知活动创建者有新的申请
        applicant = User.query.get(user_id)
        message = f"{applicant.Username} 申请加入您的活动 {event.eventName}, 申请理由: {reason}"
        notify_user(reservationUserId, user_id, event_id, message, 2)  # 申请消息

        return jsonify({"status": "Success", "message": "申请已提交等待审批"}), 200
    else:
        # 如果活动不需要审批，则直接添加用户到活动，并设置状态为1
        user_event = UserEvent(userID=user_id, eventID=event_id)
        db.session.add(user_event)
        db.session.commit()

        # 通知活动创建者有新的成员加入
        new_member = User.query.get(user_id)
        message = f"{new_member.Username} 加入了您的活动 {event.eventName}"
        notify_user(reservationUserId, user_id, event_id, message, 1)  # 系统消息

        return jsonify({"status": "Success", "message": "成功加入活动"}), 200

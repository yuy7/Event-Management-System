from flask import jsonify, request
from Dao.TempEvent import Event
from Dao.Application import Application
from Dao.UserEvent import UserEvent  # 确保你已经在Dao中导入了UserEvent
from Dao.User import User  # 确保你已经在Dao中导入了User
from Dao.Notification import Notification  # 确保你已经在Dao中导入了Notification
from __init__ import db

def notify_user(recipient_id, sender_id, event_id, message):
    notification = Notification(
        recipient_id=recipient_id,
        sender_id=sender_id,
        event_id=event_id,
        message=message
    )
    db.session.add(notification)
    db.session.commit()

def apply_event():
    # data = request.get_json()
    # user_id = data.get("userID")
    # event_id = data.get("eventID")
    user_id = 251101163
    event_id = 5

    # 检查活动是否存在
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"status": "Error", "message": "活动不存在"}), 404

    # 获取活动创建者ID
    creator_id = event.creator_id  #TODO

    if event.requireApproval:
        # 如果活动需要审批，则创建申请记录
        application = Application(eventID=event_id, userID=user_id, status='pending')
        db.session.add(application)
        db.session.commit()

        # 通知活动创建者有新的申请
        applicant = User.query.get(user_id)
        message = f"{applicant.username} 申请加入您的活动 {event.eventName}"
        notify_user(creator_id, user_id, event_id, message)

        return jsonify({"status": "Success", "message": "申请已提交等待审批"}), 200
    else:
        # 如果活动不需要审批，则直接添加用户到活动
        user_event = UserEvent(userID=user_id, eventID=event_id)
        db.session.add(user_event)
        db.session.commit()

        # 通知活动创建者有新的成员加入
        new_member = User.query.get(user_id)
        message = f"{new_member.username} 加入了您的活动 {event.eventName}"
        notify_user(creator_id, user_id, event_id, message)

        return jsonify({"status": "Success", "message": "成功加入活动"}), 200

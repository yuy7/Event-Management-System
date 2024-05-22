from flask import jsonify, request
from Dao.Event import Event
from Dao.Application import Application
from Dao.UserEvent import UserEvent  # 确保你已经在Dao中导入了UserEvent
from __init__ import db

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

    if event.requireApproval:
        # 如果活动需要审批，则创建申请记录
        application = Application(eventID=event_id, userID=user_id, status='pending')
        db.session.add(application)
        db.session.commit()
        return jsonify({"status": "Success", "message": "申请已提交等待审批"}), 200
    else:
        # 如果活动不需要审批，则直接添加用户到活动
        user_event = UserEvent(userID=user_id, eventID=event_id)
        db.session.add(user_event)
        db.session.commit()
        return jsonify({"status": "Success", "message": "成功加入活动"}), 200

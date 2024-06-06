from flask import jsonify, request, session
from __init__ import db
from Dao.Notification import Notification
from Dao.UserAddEvent import UserAddEvent


def getSystemNotifications():
    # 获取当前用户的 ID
    # user_id = session.get("userid")
    user_id = request.args.get("userid")
    # 查询通知
    notifications = Notification.query.filter(
            Notification.recipient_id==user_id, 
            Notification.type==1
        ).order_by(Notification.timestamp.desc()).all()
    # 更新未读通知为已读
    for notification in notifications:
        if not notification.read:
            notification.read = True
            db.session.commit()
    
    # 构建通知列表
    notifications_list = [{
        'id': notification.id,
        'sender_id': notification.sender_id,
        'event_id': notification.event_id,
        'message': notification.message,
        'read': notification.read,
        'type': notification.type,
        'timestamp': notification.timestamp.strftime('%Y-%m-%d %H:%M:%S')  # 格式化时间戳

    } for notification in notifications]
    print(notifications_list)
    return jsonify(notifications_list)

def getApprovalNotifications():
    # 获取当前用户的 ID
    # user_id = session.get("userid")
    user_id = request.args.get("userid")
    # 查询通知
    notifications = Notification.query.filter(
            Notification.recipient_id==user_id, 
            Notification.type==2
        ).order_by(Notification.timestamp.desc()).all()
    
    # 更新未读通知为已读
    for notification in notifications:
        if not notification.read:
            notification.read = True
            db.session.commit()
    
    # 构建通知列表
    notifications_list = [{
        'id': notification.id,
        'sender_id': notification.sender_id,
        'event_id': notification.event_id,
        'message': notification.message,
        'read': notification.read,
        'type': notification.type,
        'timestamp': notification.timestamp.strftime('%Y-%m-%d %H:%M:%S')  # 格式化时间戳

    } for notification in notifications]
    print(notifications_list)
    return jsonify(notifications_list)

def acceptEventApply():
    eventApplyID = request.json.get("notificationID")
    # 修正命名错误：从roleApply到eventApply
    eventApply = Notification.query.filter_by(id=eventApplyID).first()
    if not eventApply:
        return jsonify({
            "status": "Error",
            "message": "Event apply not found"
        }), 404
    
    try:
        # 添加：设置UserAddEvent的state为1（代表接受）
        userAddEvent = UserAddEvent.query.filter(
                UserAddEvent.userID==eventApply.sender_id, 
                UserAddEvent.eventID==eventApply.event_id
            ).first()
        if userAddEvent:
            userAddEvent.state = 1

        # 添加：设置Notification的read为1（代表已读）
        notification = Notification.query.filter_by(id=eventApplyID).first()
        if notification:
            notification.read = 1

        # 删除的是eventApply，之前代码中的roleApply
        # db.session.delete(eventApply)

        db.session.commit()
        return jsonify({
            "status": "Success"
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "Error",
            "message": str(e)
        }), 500
    
def refuseEventApply():
    eventApplyID = request.json.get("notificationID")
    # 修正命名错误：从roleApply到eventApply
    eventApply = Notification.query.filter_by(id=eventApplyID).first()
    if not eventApply:
        return jsonify({
            "status": "Error",
            "message": "Event apply not found"
        }), 404
    
    try:
        # 添加：设置UserAddEvent的state为1（代表接受）
        userAddEvent = UserAddEvent.query.filter(
                UserAddEvent.userID==eventApply.sender_id, 
                UserAddEvent.eventID==eventApply.event_id
            ).first()
        if userAddEvent:
            userAddEvent.state = 2

        # 添加：设置Notification的read为1（代表已读）
        notification = Notification.query.filter_by(id=eventApplyID).first()
        if notification:
            notification.read = 1

        # 删除的是eventApply，之前代码中的roleApply
        # db.session.delete(eventApply)

        db.session.commit()
        return jsonify({
            "status": "Success"
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "Error",
            "message": str(e)
        }), 500
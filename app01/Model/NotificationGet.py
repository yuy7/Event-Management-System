from flask import jsonify, request, session
from __init__ import db
from Dao.Notification import Notification


def get_notifications():
    # 获取当前用户的 ID
    user_id = session.get("userID")
    
    # 查询通知
    notifications = Notification.query.filter_by(recipient_id=user_id).order_by(Notification.timestamp.desc()).all()
    
    # 构建通知列表
    notifications_list = [{
        'id': notification.id,
        'recipient_id': notification.recipient_id,
        'sender_id': notification.sender_id,
        'event_id': notification.event_id,
        'message': notification.message,
        'read': notification.read,
        'timestamp': notification.timestamp
    } for notification in notifications]
    
    return jsonify(notifications_list)

from flask import jsonify, request, session
from __init__ import db
from Dao.Notification import Notification


def get_notifications():
    # 获取当前用户的 ID
    # user_id = session.get("userid")
    user_id = request.args.get("userid")
    print(user_id)
    # 查询通知
    notifications = Notification.query.filter_by(recipient_id=user_id).order_by(Notification.timestamp.desc()).all()
    
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

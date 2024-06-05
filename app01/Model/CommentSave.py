from flask import request, jsonify
from Dao.Comment import Comment
from Dao.User import User
from Dao.Event import Event  # 确保导入 Event 模型
from __init__ import db
from datetime import datetime

def add_comment():
    data = request.get_json()
    user_id = data.get('userId')
    answer = data.get('answer')
    ans_time = data.get('ansTime')
    event_id = data.get('eventID')
    
    # 检查是否提供了 event_id
    if not event_id:
        return jsonify({'error': 'EventID cannot be null'}), 400
    
    # 查找事件
    event = Event.query.get(event_id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    
    # 转换 ans_time 为 MySQL 认可的格式
    try:
        ans_time = ans_time.replace('Z', '')  # 去掉 'Z'
        dt = datetime.fromisoformat(ans_time)
        mysql_datetime_str = dt.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({'error': 'Invalid datetime format'}), 400
    
    # 查找用户
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # 创建评论
    comment = Comment(
        UserID=user_id,
        Username=user.Username,
        Answer=answer,
        AnsTime=mysql_datetime_str,
        EventID=event_id  # 确保提供了有效的 EventID
    )
    
    db.session.add(comment)
    db.session.commit()
    
    return jsonify({'message': 'Comment added successfully'}), 200

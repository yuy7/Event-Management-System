from flask import request, jsonify
from Dao.Comment import Comment
from Dao.User import User


from __init__ import db

def add_comment():
    data = request.get_json()
    user_id = data.get('userId')
    answer = data.get('answer')
    ans_time = data.get('ansTime')
    
    # 查找用户
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # 创建评论
    comment = Comment(
        UserID=user_id,
        Username=user.Username,
        Answer=answer,
        AnsTime=ans_time
    )
    
    db.session.add(comment)
    db.session.commit()
    
    return jsonify({'message': 'Comment added successfully'}), 200
from flask import jsonify, request
from __init__ import db
from Dao.Comment import Comment

def format_comment(comment):
    return {
        "comment_id": comment.CommentID,
        "username": comment.Username,
        "answer": comment.Answer,
        "ans_time": comment.AnsTime.strftime('%Y-%m-%d %H:%M:%S'),  # 格式化时间戳
        "ans": []
    }

def format_answer(answer):
    return {
        "ansUser": answer.Username,
        "answer": answer.Answer,
        "ansTime": answer.AnsTime.strftime('%Y-%m-%d %H:%M:%S'),  # 格式化时间戳
    }

def getComment():
    print('----------------')
    event_id = request.args.get('eventID')
    if not event_id:
        return jsonify({"status": "Error", "message": "Missing eventID"}), 400
    
    # 获取特定事件的所有评论
    comments_query = Comment.query.filter_by(EventID=event_id).all()
    
    # 构建评论字典，键为CommentID, 值为评论对象
    comments_dict = {}
    for comment in comments_query:
        if comment.AnswerTo is None:  # 这是一个主评论
            comments_dict[comment.CommentID] = format_comment(comment)
    
    # 添加评论的回复
    for comment in comments_query:
        if comment.AnswerTo is not None:  # 这是一个回复
            parent_comment = comments_dict.get(comment.AnswerTo)
            if parent_comment:
                parent_comment['ans'].append(format_answer(comment))
    
    # 整理数据
    result = list(comments_dict.values())
    
    # 返回JSON结果
    return jsonify(result)

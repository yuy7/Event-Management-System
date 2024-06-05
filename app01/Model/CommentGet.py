from flask import jsonify, request
from __init__ import db
from Dao.Comment import Comment

def get_comments():
   
    event_id = request.args.get("eventid")


    if event_id:
        comments = Comment.query.filter_by(EventID=event_id).order_by(Comment.AnsTime.desc()).all()
    else:
        return jsonify([])



    # 构建评论列表
    comments_list = [{
        'comment_id': comment.CommentID,
        'user_id': comment.UserID,
        'username': comment.Username,
        'answer': comment.Answer,
        'ans_time': comment.AnsTime,
        'event_id': comment.EventID
    } for comment in comments]

    return jsonify(comments_list)

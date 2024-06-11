from flask import Flask, jsonify, request
import os
from werkzeug.utils import secure_filename
from Dao.Event import Event
from Dao.EventDetail import EventDetail
from Dao.EventFeedback import EventFeedback
from datetime import datetime
from Dao.UserEvent import UserEvent
from Dao.User import User
from Dao.EventImage import EventImage
from __init__ import db
from Tool.Mappings import time_mapping
app = Flask(__name__)

def get_event():
    data = request.get_json()

    if not data:
        return jsonify({
            "status": "Failure",
            "message": "No input data provided"
        }), 400

    event_id = data.get("eventID")
    
    if not event_id:
        return jsonify({
            "status": "Failure",
            "message": "Event ID is required"
        }), 400

    # 查询数据库中是否存在对应的event
    event = Event.query.filter_by(eventID=event_id).first()
    
    if not event:
        return jsonify({
            "status": "Failure",
            "message": "Event not found"
        }), 404

    # 查询活动详情
    event_detail = EventDetail.query.filter_by(eventID=event_id).first()
    time_slot = time_mapping.get(event.time, "未知时间段")
    
    # 获取活动参与者的用户名
    participants = UserEvent.query.filter_by(eventID=event_id).all()
    participant_usernames = []
    for participant in participants:
        user = User.query.filter_by(UserID=participant.userID).first()
        if user:
            participant_usernames.append(user.Username)

    # Fetch images associated with the event
    # event_images = EventImage.query.filter_by(eventID=event_id).all()
    # image_paths = [img.image_path for img in event_images]

    # 返回活动的相关信息
    event_info = {
        "eventID": event.eventID,
        "eventName": event.eventName,
        "date": event.date,
        "reservationUserId": event.reservationUserId,
        "eventTypeID": event.eventTypeID,
        "numberOfPeople": event.numberOfPeople,
        "preferredLocation": event.preferredLocation,
        "arrangedLocation": event.arrangedLocation,
        "requireApproval": event.requireApproval,
        "time": time_slot,
        "description": event_detail.description if event_detail else None,
        "notification": event_detail.notification if event_detail else None,
        "participants": participant_usernames,
        # "images": image_paths
    }

    return jsonify({
        "status": "Success",
        "event": event_info
    }), 200

def uploadImage():
    if 'file' not in request.files:
        return jsonify({
            "status": "Failure",
            "message": "No file part"
        }), 400

    file = request.files['file']
    event_id = request.form.get("eventID")
    
    if not event_id:
        return jsonify({
            "status": "Failure",
            "message": "Event ID is required"
        }), 400

    if file.filename == '':
        return jsonify({
            "status": "Failure",
            "message": "No selected file"
        }), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER', filename])
        file.save(file_path)
        
        # Saving the file path to database
        event_image = EventImage(eventID=event_id, image_path=file_path)
        db.session.add(event_image)
        db.session.commit()

        return jsonify({
            "status": "Success",
            "message": "File uploaded successfully",
            "file_path": file_path
        }), 200
    else:
        return jsonify({
            "status": "Failure",
            "message": "File upload failed"
        }), 500

def getResult():
    return '2024年5月27日，我们在逸夫楼102举行了年级会，现场气氛活跃，活动顺利开展！'

def getUserRole():
    data = request.get_json()
    event_id = data.get("eventid")
    user_id = data.get("userid")
    event = Event.query.filter(Event.eventID==event_id, Event.reservationUserId==user_id).all()
    if len(event) > 0:
        return 'reservationUser'
    else: 
        return 'participant'

def getAllFeedback():
    data = request.get_json()
    event_id = data.get("eventid")
    feedback_query = EventFeedback.query.filter_by(eventID=event_id).all()
    # 转换查询结果为列表的字典形式
    feedbackList = [
        {
            'feedbackId': feedback.feedbackId,
            'userID': feedback.userID,
            'eventID': feedback.eventID,
            'feedback': feedback.feedback,
            'feedbackTime': feedback.feedbackTime.strftime("%Y-%m-%d %H:%M:%S") if feedback.feedbackTime else None
        } for feedback in feedback_query
    ]

    # 使用jsonify返回JSON数据
    return jsonify(feedbackList), 200

def submitFeedback():
    data = request.get_json()
    event_id = data.get("eventid")
    user_id = data.get("userid")
    feedback = data.get("feedback")
    feedback_time = datetime.now()

    # 创建EventFeedback对象，加入时间戳
    feedback_entry = EventFeedback(userID=user_id, eventID=event_id, feedback=feedback, feedbackTime=feedback_time)

    # 将对象添加到session并提交到数据库
    db.session.add(feedback_entry)
    db.session.commit()

    return jsonify({"success": True, "message": "Feedback submitted successfully"}), 200
    
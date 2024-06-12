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
from werkzeug.utils import secure_filename
from __init__ import db
from Tool.Mappings import time_mapping


UPLOAD_FOLDER = 'app01\image'

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
    try:
        if 'image' not in request.files:
            return jsonify({'status': 'Error', 'message': 'No file part'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'status': 'Error', 'message': 'No selected file'}), 400
        
        eventid = request.form.get('eventid')  # 获取 eventid 字段
        # 检查数据库中是否已存在相同 eventID 的记录
        existing_image = EventImage.query.filter_by(eventID=eventid).first()
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if existing_image:
            # 更新现有记录
            existing_image.image_path = filepath
            existing_image.uploaded_at = datetime.now()
        else:
            # 创建新记录
            new_image = EventImage(eventID=eventid, image_path=filepath, uploaded_at=datetime.now())
            db.session.add(new_image)
        
        # 保存上传的图片到指定文件夹
        file.save(filepath)
        
        db.session.commit()  # 提交数据库事务
        
        # 返回上传成功的响应给前端
        return jsonify({'status': 'Success', 'message': 'Image uploaded successfully', 'image_path': filename, 'eventid': eventid}), 200
    except Exception as e:
        print(f"Error uploading image: {e}")
        db.session.rollback()  # 回滚数据库事务
        return jsonify({'status': 'Error', 'message': 'Failed to upload image'}), 500
    

def getQrCode():
    

def getResultTemplate():
    event_id = request.args.get("eventid")
    # 从数据库中获取指定ID的活动信息
    event = Event.query.filter_by(eventID = event_id).first()

    if event is None:
        return "指定的活动不存在。"

    # 准备模板，并填充活动信息
    template = (
        f"{event.date}，我们在{event.arrangedLocation or event.preferredLocation}举行了{event.eventName}，"
        f"现场气氛活跃，参加人数为{event.numberOfPeople}人，活动顺利开展！"
    )

    return template

def saveResult():
    # 从请求中获取 result 和 event_id
    # result = request.args.get("result")
    # event_id = request.args.get("eventid")
    data = request.get_json()
    result = data.get("result")
    event_id = data.get("eventid")
    # print(event_id)
    # 检查是否提供了必要的信息
    if not result or not event_id:
        return jsonify({'error': 'Missing result or event_id'}), 400

    # 查找 event detail 对象
    event_detail = db.session.query(EventDetail).filter(EventDetail.eventID == event_id).first()

    # 如果该 event detail 不存在，则创建一个新的
    if not event_detail:
        event_detail = EventDetail(eventID=event_id, result=result)
        db.session.add(event_detail)
    else:
        # 更新 result 属性
        event_detail.result = result

    # 提交更改到数据库
    db.session.commit()

    return jsonify({'message': 'Result saved successfully'}), 200

def getResult():
    event_id = request.args.get("eventid")

    # 检查是否提供了必要的 event_id
    if not event_id:
        return jsonify({'error': 'Missing event_id'}), 400

    # 查找 event detail 对象
    event_detail = db.session.query(EventDetail).filter(EventDetail.eventID == event_id).first()

    if not event_detail or not event_detail.result:
        return ''
    else:
        return event_detail.result

def getUserRole():
    # data = request.get_json()
    # event_id = data.get("eventid")
    # user_id = data.get("userid")
    user_id = request.args.get("userid")
    event_id = request.args.get("eventid")
    event = Event.query.filter(Event.eventID==event_id, Event.reservationUserId==user_id).all()
    print(user_id)
    print(event_id)
    if len(event) > 0:
        return 'reservationUser'
    else: 
        return 'participant'

def getAllFeedback():
    # data = request.get_json()
    # event_id = data.get("eventid")
    event_id = request.args.get("eventid")
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
    
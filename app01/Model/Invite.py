from flask import Flask, jsonify, request
from __init__ import db
from Dao.Event import Event
from Dao.User import User
from Dao.Class import Class
from Dao.InvitedList import InvitedList

def invite():
    data = request.get_json()
    invite_type = data.get('inviteType')
    event_id = data.get('eventID')
    invited_id = data.get('invitedID')

    # 检查事件是否存在
    event = Event.query.filter_by(eventID=event_id).first()
    if not event:
        return jsonify({'message': 'Event not found'}), 404

    # 检查被邀请对象是否存在
    if invite_type == 1:  # 个人
        invited = User.query.filter_by(UserID=invited_id).first()
        if not invited:
            return jsonify({'message': 'User not found'}), 404
    elif invite_type == 2:  # 班级
        invited = Class.query.filter_by(ClassID=invited_id).first()
        if not invited:
            return jsonify({'message': 'Class not found'}), 404
    else:
        return jsonify({'message': 'Invalid inviteType'}), 400

    # 创建邀请记录
    invite_record = InvitedList(inviteType=invite_type, eventID=event_id, invitedID=invited_id)
    db.session.add(invite_record)
    db.session.commit()

    return jsonify({'message': 'Invite sent successfully'}), 200

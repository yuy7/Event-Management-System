from flask import Flask, jsonify, request
from Dao.TempEvent import Event
from Dao.User import User
from Dao.InvitedList import InvitedList, db  # 导入模型和数据库实例

def invite():
    data = request.get_json()
    invite_type = data.get('inviteType')
    event_id = data.get('eventID')
    invited_ids = data.get('invitedIDs')  # 改为复数形式，表示多个ID

    # 检查事件是否存在
    event = Event.query.filter_by(eventID=event_id).first()
    if not event:
        return jsonify({'message': 'Event not found'}), 404

    if invite_type == 1:  # 个人
        for invited_id in invited_ids:
            invited = User.query.filter_by(UserID=invited_id).first()
            if not invited:
                return jsonify({'message': f'User with ID {invited_id} not found'}), 404
            # 创建邀请记录
            invite_record = InvitedList(inviteType=invite_type, eventID=event_id, invitedID=invited_id)
            db.session.add(invite_record)
        
    # 班级类还没有相应的实现
    # elif invite_type == 2:  # 班级
    #     for invited_id in invited_ids:
    #         invited = Class.query.filter_by(classID=invited_id).first()
    #         if not invited:
    #             return jsonify({'message': f'Class with ID {invited_id} not found'}), 404
    #         # 创建邀请记录
    #         invite_record = InvitedList(inviteType=invite_type, eventID=event_id, invitedID=invited_id)
    #         db.session.add(invite_record)
    
    else:
        return jsonify({'message': 'Invalid inviteType'}), 400

    db.session.commit()
    return jsonify({'message': 'Invitations sent successfully'}), 200

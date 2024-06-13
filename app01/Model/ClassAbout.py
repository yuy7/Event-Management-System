from flask import Flask, jsonify, request
from __init__ import db
from Dao.Class import Class, ClassUser
from Dao.User import User

def get_class_list():
    classes = Class.query.all()
    class_list = [{'classID': c.ClassID, 'className': c.ClassName} for c in classes]
    return jsonify(class_list), 200

def get_class_students():
    class_id = request.args.get('ClassID')
    if not class_id:
        return jsonify({'message': '缺少班级ID'}), 400
    
    class_users = ClassUser.query.filter_by(ClassID=class_id).all()
    if not class_users:
        return jsonify({'message': '该班级没有找到学生'}), 404
    
    students_list = [{'userID': cu.UserID, 'username': User.query.get(cu.UserID).Username} for cu in class_users]
    return jsonify(students_list), 200

def add_student_to_class():
    data = request.get_json()
    user_id = data.get('userID')
    class_id = data.get('ClassID')
    
    if not user_id or not class_id:
        return jsonify({'message': '缺少用户ID或班级ID'}), 400
    
    # 检查用户是否存在
    user = User.query.filter_by(UserID=user_id).first()
    if not user:
        return jsonify({'message': '未找到该用户'}), 404
    
    class_user = ClassUser(UserID=user_id, ClassID=class_id)
    db.session.add(class_user)
    db.session.commit()
    return jsonify({'message': '学生添加成功'}), 200

def remove_student_from_class():
    data = request.get_json()
    user_id = data.get('userID')
    class_id = data.get('ClassID')

    if not user_id or not class_id:
        return jsonify({'message': '缺少用户ID或班级ID'}), 400

    # 检查用户是否存在
    user = User.query.filter_by(UserID=user_id).first()
    if not user:
        return jsonify({'message': '未找到该用户'}), 404

    # 检查用户是否在该班级
    class_user = ClassUser.query.filter_by(UserID=user_id, ClassID=class_id).first()
    if not class_user:
        return jsonify({'message': '该班级未找到该学生'}), 404

    try:
        db.session.delete(class_user)
        db.session.commit()
        return jsonify({'message': '学生移除成功'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '移除学生时发生错误', 'error': str(e)}), 500
def add_class():
    data = request.get_json()
    class_name = data.get('className')
    
    if not class_name:
        return jsonify({'message': '缺少班级名称'}), 400
    
    new_class = Class(ClassName=class_name)
    db.session.add(new_class)
    db.session.commit()
    return jsonify({'message': '班级添加成功'}), 200
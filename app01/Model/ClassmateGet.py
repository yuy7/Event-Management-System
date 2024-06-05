from flask import jsonify, request
from __init__ import db
from Dao.Class import Class, ClassUser

def classmate_get():
    # 从请求中获取ClassID
    class_id = request.args.get('ClassID')
    
    if not class_id:
        return jsonify({'error': 'ClassID is required'}), 400
    
    # 查询该班级下的所有学生
    class_users = ClassUser.query.filter_by(ClassID=class_id).all()
    
    if not class_users:
        return jsonify({'error': 'No students found for this class'}), 404
    
    # 构建学生列表
    students_list = [{
        'user_id': class_user.UserID,
        'class_id': class_user.ClassID
    } for class_user in class_users]
    
    return jsonify(students_list)

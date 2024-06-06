from flask import Blueprint, jsonify, request
from Dao.User import User
from __init__ import db


def user_register():
    """
    用户注册
    :return:
    """
    data = request.get_json()
    nickname = data.get("nickname")
    phoneNumber = data.get("phoneNumber")
    email = data.get("email")
    password = data.get("password")
    # 检查手机号是否已经被注册
    existing_user = User.query.filter_by(PhoneNumber=phoneNumber).first()
    if existing_user:
        return jsonify({
            "status": "Error",
            "message": "手机号已经被注册"
        }), 400
    # 创建新用户并保存到数据库
    new_user = User(Username=nickname, PhoneNumber=phoneNumber, Password=password, Email=email)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({
        "status": "Success",
        "message": "注册成功"
    })

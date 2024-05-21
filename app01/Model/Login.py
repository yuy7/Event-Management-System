from flask import jsonify, request
from flask_jwt_extended import create_access_token
from Dao.User import User

def user_login():
    """
    用户登录
    :return:
    """
    data = request.get_json()
    phoneNumber = data.get("phoneNumber")
    password = data.get("password")

    # 查询数据库
    user = User.query.filter_by(PhoneNumber=phoneNumber).first()

    # 若用户存在且密码正确，返回成功的响应
    if user and user.Password == password:
        return jsonify({
            "status": "Success",
            "UserId": user.UserID
        })

    # 否则返回错误信息
    else:
        return jsonify({
            "status": "Error"
        })
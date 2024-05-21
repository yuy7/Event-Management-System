from flask import jsonify, request, session
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
        session["userID"] = user.UserID
        return jsonify({
            "status": "Success"
        })

    # 否则返回错误信息
    else:
        return jsonify({
            "status": "False"
        })
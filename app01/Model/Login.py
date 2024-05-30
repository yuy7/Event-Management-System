from flask import jsonify, request, session
from Model.UpdateDb import update_db
from Dao.User import User

def user_login():
    """
    用户登录
    :return:
    """
    data = request.get_json()
    phoneNumber = data.get("phoneNumber")
    password = data.get("password")
    flag = update_db()
    if flag == "Success":
        pass
    else:
        return jsonify({
            "status": "Error",
            "data": "更新场地数据库失败, 请重试"
        })
    # 查询数据库 传入的可能是电话号码或userid
    user = User.query.filter_by(PhoneNumber=phoneNumber).first()
    if user is not None:
        pass
    else:
         user = User.query.filter_by(UserID=phoneNumber).first()

    # 若用户存在且密码正确，返回成功的响应
    if user and user.Password == password:
        session["userID"] = user.UserID
        print(user.Role)
        if(user.UserID == 10086):
            return jsonify({
                "status": "Success",
                "role": "root",
                "UserId": user.UserID
            })
        else:
            print('normal')
            return jsonify({
                "status": "Success",
                "role": "normal user",
                "UserId": user.UserID
            })

    # 否则返回错误信息
    else:
        return jsonify({
            "status": "Error"
        })
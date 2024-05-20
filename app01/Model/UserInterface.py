from flask import jsonify, request, session
from Dao.User import User
from Dao.RoleApply import RoleApply
from Dao.Role import Role
from __init__ import db

# 得到当前用户信息，GET方法
def get_user():
    userID = session.get("userID")
    # userID = 251101164
    user = User.query.filter_by(UserID=userID).first()
    return jsonify({
        'UserID': user.UserID,
        'Username': user.Username,
        'Email': user.Email,
        'Phone': user.PhoneNumber,
        'Role': user.Role,
    })


# 绑定邮箱，POST方法
def bindEmail():
    userID = session.get("userID")
    # userID = 251101164
    email = request.json.get("email")
    rows = User.query.filter_by(UserID=userID).update({"Email":email})
    try:
        db.session.commit()
        if (rows == 0):
            raise Exception("No such user")
        else:
            return jsonify({
                "status": "Success"
            })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "Error",
            "message": str(e)
        }), 500


# 绑定手机号，POST方法
def bindPhone():
    userID = session.get("userID")
    # userID = 251101164
    phone = request.json.get("phone")
    rows = User.query.filter_by(UserID=userID).update({"PhoneNumber":phone})
    try:
        db.session.commit()
        if (rows == 0):
            raise Exception("No such user")
        else:
            return jsonify({
                "status": "Success"
            })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "Error",
            "message": str(e)
        }), 500


# 申请身份，POST方法
def roleApply():
    userID = session.get("userID")
    # userID = 251101164
    role = request.json.get("role")
    roleID = Role.query.filter_by(roleName=role).first().roleID
    roleApply = RoleApply(userID=userID, roleID=roleID)
    try:
        db.session.add(roleApply)
        db.session.commit()
        return jsonify({
            "status": "Success"
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "Error",
            "message": str(e)
        }), 500
    
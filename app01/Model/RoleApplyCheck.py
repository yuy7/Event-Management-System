from flask import jsonify, request, session
from Dao.User import User
from Dao.RoleApply import RoleApply
from Dao.Notification import Notification
from Dao.Role import Role
from __init__ import db

# 显示所有身份申请，GET方法
def getRoleApply():
    roleApplyList = db.session.query(RoleApply, Role.roleName).join(Role, RoleApply.roleID == Role.roleID).filter(RoleApply.roleState == 0).all()
    res = []
    for roleApply,roleName in roleApplyList:
        res.append({
            "roleApplyID": roleApply.roleApplyID,
            "userID": User.query.filter_by(UserID=roleApply.userID).first().Username,
            "roleName": roleName,
        })
    return jsonify(res)



# 超管接受身份申请，POST方法
def acceptRoleApply():
    roleApplyID = request.json.get("roleApplyID")
    print(roleApplyID)
    roleApply = RoleApply.query.filter_by(roleApplyID=roleApplyID).first()
    user = User.query.filter_by(UserID=roleApply.userID).first()
    user.Role = Role.query.filter_by(roleID=roleApply.roleID).first().roleName
    try:
        db.session.delete(roleApply)
        db.session.commit()
        return jsonify({
            "status": "Success"
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "Error",
            "message": str(e)
        }), 500

# 超管拒绝身份申请，POST方法
def refuseRoleApply():
    roleApplyID = request.json.get("roleApplyID")
    roleApply = RoleApply.query.filter_by(roleApplyID=roleApplyID).first()
    roleName = Role.query.filter_by(roleID=roleApply.roleID).first().roleName
    user = User.query.filter_by(UserID=roleApply.userID).first()
    notification = Notification(
        recipient_id=user.UserID,
        sender_id=user.UserID,
        message=f"您的 {roleName} 身份申请被驳回",
        type=1  # 传入通知类型
    )
    user.Role = "无"
    try:
        db.session.add(notification)
        db.session.delete(roleApply)
        db.session.commit()
        return jsonify({
            "status": "Success"
        })
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({
            "status": "Error",
            "message": str(e)
        }), 500
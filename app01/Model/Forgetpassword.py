from flask import Flask, request, jsonify
from __init__ import db
from Dao.User import User  # 确保正确导入User模型

app = Flask(__name__)


def forget_password():
    data = request.json
    email = data.get('email')
    verificationCode = data.get('verificationCode')
    new_password = data.get('password')
    # print(verificationCode)

    user = User.query.filter_by(Email=email).first()

    if user and user.VerificationCode == verificationCode:
        user.Password = new_password
        user.VerificationCode = None  # 清除验证码
        db.session.commit()
        return jsonify({'status': 'Password reset successfully'}), 200
    else:
        return jsonify({'status': 'Invalid verification code or email'}), 400

# 启动应用

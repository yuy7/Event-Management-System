import os
from flask import Flask, jsonify, request
from flask_cors import CORS


from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from Model.Login import user_login
from __init__ import init_db

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)
# username: root, password: root
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/emsdb?charset=utf8'
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'User'
    UserID = db.Column('UserID', db.Integer, primary_key=True)
    Username = db.Column('Username', db.String(50))
    Password = db.Column('Password', db.String(100))
    Email = db.Column('Email', db.String(100))
    PhoneNumber = db.Column('PhoneNumber', db.String(20))
    Role = db.Column('Role', db.String(20))
    VerificationCode = db.Column('VerificationCode', db.String(20))
    RegistrationTime = db.Column('RegistrationTime', db.TIMESTAMP, default=db.func.current_timestamp())
    LastLoginTime = db.Column('LastLoginTime', db.TIMESTAMP)
    AccountStatus = db.Column('AccountStatus', db.String(20))

# @app.route("/login", methods=["POST"])
# def login_router():
#     return user_login(request)

@app.route("/login", methods=["POST"])
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
            "status": "Success"
        })

    # 否则返回错误信息
    else:
        return jsonify({
            "status": "False"
        })

if __name__ == "__main__":
    app.run(debug=True)

    
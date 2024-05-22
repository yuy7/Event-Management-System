from flask import Flask
from flask_cors import CORS
from __init__ import db
from Model.Login import user_login
from Model.EventCreate import EventCreate
from Model.EventManage import get_events
from Model.UserInterface import get_user,bindEmail,bindPhone,roleApply
from Model.Invite import invite
from flask_jwt_extended import JWTManager, jwt_required
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)
# username: root, password: root
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/emsdb?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False  # 设置为 True 在生产环境中

db.init_app(app)
app.route("/login", methods=["POST"])(user_login)
app.route("/eventCreate", methods=["POST"])(EventCreate)
app.route("/events", methods=["GET"])(get_events)
app.route("/userinterface", methods=["GET"])(get_user)
app.route("/userinterface/bindEmail", methods=["POST"])(bindEmail)
app.route("/userinterface/bindPhone", methods=["POST"])(bindPhone)
app.route("/userinterface/roleApply", methods=["POST"])(roleApply)
app.route("/invite", methods=["POST"])(invite)

if __name__ == "__main__":
    app.run(debug=True)
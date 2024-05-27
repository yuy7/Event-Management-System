from flask import Flask
from flask_cors import CORS
from Model.Login import user_login
from Model.EventCreate import EventCreate
from Model.EventManage import get_events,getUserEvent,deleteEvent
from Model.UserInterface import get_user,bindEmail,bindPhone,roleApply,get_users
from Model.Invite import invite
from Model.ApplyEvent import apply_event
from Model.LocationArrange import locationArrange, getUnarrangedEvents, getArrangedEvents
from Model.RoleApplyCheck import acceptRoleApply, getRoleApply
from Model.NotificationGet import get_notifications
from flask_jwt_extended import JWTManager, jwt_required
import os

from app01 import db
from app01.Model.budgetview import budget_blueprint

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)
# username: root, password: root
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/activitymanagementsystemdb?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False  # 设置为 True 在生产环境中

db.init_app(app)
app.route("/login", methods=["POST"])(user_login)
app.route("/eventCreate", methods=["POST"])(EventCreate)
app.route("/events", methods=["GET"])(get_events)
app.route("/getUserEvent", methods=["GET"])(getUserEvent)
app.route("/deleteEvent", methods=["POST"])(deleteEvent)
app.route("/userinterface", methods=["GET"])(get_user)
app.route("/userinterface/bindEmail", methods=["POST"])(bindEmail)
app.route("/userinterface/bindPhone", methods=["POST"])(bindPhone)
app.route("/userinterface/roleApply", methods=["POST"])(roleApply)
app.route("/userinterface/get_users", methods=["GET"])(get_users)
app.route("/invite", methods=["POST"])(invite)
app.route("/applyEvent", methods=["POST"])(apply_event)
app.route("/locationArrange", methods=["POST"])(locationArrange)
app.route("/acceptRoleApply", methods=["POST"])(acceptRoleApply)
app.route("/roleApplyCheck", methods=["GET"])(getRoleApply)             
app.route("/getUnarrangedEvents", methods=["GET"])(getUnarrangedEvents)    
app.route("/getArrangedEvents", methods=["GET"])(getArrangedEvents)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
app.route("/notifications", methods=["GET"])(get_notifications)
app.register_blueprint(budget_blueprint, url_prefix='/budget')

if __name__ == "__main__":
    app.run(debug=True)

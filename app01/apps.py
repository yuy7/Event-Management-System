from flask import Flask
from flask_cors import CORS
from Model.Login import user_login
from Model.EventCreate import EventCreate, getLocationList
from Model.EventManage import get_events, getUserEvent, deleteEvent, getUserAddEvent
from Model.UserInterface import get_user, bindEmail, bindPhone, roleApply, get_users
from Model.Invite import invite
from Model.ApplyEvent import apply_event, applyEventWithReason
from Model.LocationArrange import locationArrange, getUnarrangedEvents, getArrangedEvents
from Model.RoleApplyCheck import acceptRoleApply, getRoleApply, refuseRoleApply
from Model.NotificationGet import getSystemNotifications, getApprovalNotifications, acceptEventApply, refuseEventApply
from Model.EventSearch import search_events
from Model.Budgetview import set_budget, get_budget
from Model.HistoryEvent import getHistoryEvents
from Model.GetEventDetails import get_event
from Model.CommentGet import get_comments
from Model.CommentSave import add_comment
# from flask_socketio import SocketIO, send
import os
from __init__ import db
from Model.Email import send_code
from Model.Register import user_register


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)

# socketio = SocketIO(app, cors_allowed_origins="*")
# username: root, password: root
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/emsdb?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False  # 设置为 True 在生产环境中

db.init_app(app)
app.route("/login", methods=["POST"])(user_login)
app.route("/register", methods=["POST"])(user_register)
app.route("/getLocationList", methods=["GET"])(getLocationList)
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
app.route("/applyEventWithReason", methods=["POST"])(applyEventWithReason)
app.route("/locationArrange", methods=["POST"])(locationArrange)
app.route("/refuseRoleApply", methods=["POST"])(refuseRoleApply)
app.route("/acceptRoleApply", methods=["POST"])(acceptRoleApply)
app.route("/roleApplyCheck", methods=["GET"])(getRoleApply)             
app.route("/getUnarrangedEvents", methods=["GET"])(getUnarrangedEvents)    
app.route("/getArrangedEvents", methods=["GET"])(getArrangedEvents)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
app.route("/getSystemNotifications", methods=["GET"])(getSystemNotifications)
app.route("/getApprovalNotifications", methods=["GET"])(getApprovalNotifications)
app.route("/acceptEventApply", methods=["POST"])(acceptEventApply)
app.route("/refuseEventApply", methods=["POST"])(refuseEventApply)
app.route("/searchEvents", methods=["GET"])(search_events)
app.route('/budget/set', methods=['POST'])(set_budget)
app.route('/budget', methods=['GET', 'PATCH', 'PUT', 'POST'])(get_budget)
app.route('/send-code', methods=['POST'])(send_code)
app.route('/eventsJoin', methods=['GET'])(getUserAddEvent)
app.route('/history', methods=['GET'])(getHistoryEvents)

app.route("/getEventDetails", methods=["POST"])(get_event)
app.route("/getcomments", methods=["GET"])(get_comments)
app.route("/addcomment", methods=["POST"])(add_comment)
# @socketio.on("message")
# def handle_message(msg):
#     print("Message: " + msg)
#     send(msg, broadcast=True)


if __name__ == "__main__":
    # socketio.run(app, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True)
    app.run(debug=True)

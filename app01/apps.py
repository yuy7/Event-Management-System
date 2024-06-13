from flask import Flask
from flask_cors import CORS
# from flask_socketio import SocketIO, send
import os
from __init__ import db

current_path = os.getcwd()
# 检查当前路径是否包含 'app01'
if 'app01' in current_path:
    UPLOAD_FOLDER = 'image'
else:
    UPLOAD_FOLDER = 'app01/image'


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
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db.init_app(app)
# Login
from Model.Login import user_login
app.route("/login", methods=["POST"])(user_login)
# register
from Model.Register import user_register
app.route("/register", methods=["POST"])(user_register)
# EventCreate
from Model.EventCreate import EventCreate, getLocationList, getEventTypeList
app.route("/getLocationList", methods=["GET"])(getLocationList)
app.route("/eventCreate", methods=["POST"])(EventCreate)
app.route("/getEventTypeList", methods=["GET"])(getEventTypeList)
# EventManage
from Model.EventManage import get_events, getUserEvent, deleteEvent, getUserAddEvent,getUserAllEvent
app.route("/events", methods=["GET"])(get_events)
app.route("/getUserEvent", methods=["GET"])(getUserEvent)
app.route("/getUserAllEvent",methods=["GET"])(getUserAllEvent)   #得到用户所有加入和创建的活动
app.route("/deleteEvent", methods=["POST"])(deleteEvent)
app.route('/eventsJoin', methods=['GET'])(getUserAddEvent)
# UserInterface
from Model.UserInterface import get_user, bindEmail, bindPhone, roleApply, get_users
app.route("/userinterface", methods=["GET"])(get_user)
app.route("/userinterface/bindEmail", methods=["POST"])(bindEmail)
app.route("/userinterface/bindPhone", methods=["POST"])(bindPhone)
app.route("/userinterface/roleApply", methods=["POST"])(roleApply)
app.route("/userinterface/get_users", methods=["GET"])(get_users)
# Invite
from Model.Invite import invite,acceptInvite,refuseInvite,getValidationNotifications, get_invite_users, force_invite, get_available_users
app.route("/getInviteUserList", methods=["GET"])(get_invite_users)
app.route("/invite", methods=["POST"])(invite)
app.route("/forceInvite", methods=["POST"])(force_invite)
app.route("/getAvailableUsers", methods=["GET"])(get_available_users)
# ApplyEvent
from Model.ApplyEvent import apply_event, applyEventWithReason
app.route("/applyEvent", methods=["POST"])(apply_event)
app.route("/applyEventWithReason", methods=["POST"])(applyEventWithReason)
# LocationArrange
from Model.LocationArrange import locationArrange, getUnarrangedEvents, getArrangedEvents
app.route("/locationArrange", methods=["POST"])(locationArrange)
app.route("/getUnarrangedEvents", methods=["GET"])(getUnarrangedEvents)
app.route("/getArrangedEvents", methods=["GET"])(getArrangedEvents)
# RoleApplyCheck
from Model.RoleApplyCheck import acceptRoleApply, getRoleApply, refuseRoleApply
app.route("/refuseRoleApply", methods=["POST"])(refuseRoleApply)
app.route("/acceptRoleApply", methods=["POST"])(acceptRoleApply)
app.route("/roleApplyCheck", methods=["GET"])(getRoleApply)
# NotificationGet
from Model.NotificationGet import getSystemNotifications, getApprovalNotifications, acceptEventApply, refuseEventApply
app.route("/getSystemNotifications", methods=["GET"])(getSystemNotifications)
app.route("/getApprovalNotifications", methods=["GET"])(getApprovalNotifications)
app.route("/acceptEventApply", methods=["POST"])(acceptEventApply)
app.route("/refuseEventApply", methods=["POST"])(refuseEventApply)
# EventSearch
from Model.EventSearch import search_events
app.route("/searchEvents", methods=["GET"])(search_events)
# Budgetview
from Model.Budgetview import set_budget, get_budget, get_event_by_user, get_budget_app, get_event_by_app_user
app.route('/budget/set', methods=['POST'])(set_budget)
app.route('/budget', methods=['GET', 'PATCH', 'PUT', 'POST', 'DELETE'])(get_budget)
app.route('/budget_app', methods=['GET', 'PATCH', 'PUT', 'POST'])(get_budget_app)
app.route('/budget_user', methods=['GET'])(get_event_by_user)
app.route('/budget_user_app', methods=['GET'])(get_event_by_app_user)
# Email
from Model.Email import send_code
app.route('/send-code', methods=['POST'])(send_code)
# Forgetpassword
from Model.Forgetpassword import forget_password
app.route('/forgetpassword', methods=['POST'])(forget_password)
# HistoryEvent
from Model.HistoryEvent import getHistoryEvents
app.route('/history', methods=['GET'])(getHistoryEvents)
# GetEventDetails
from Model.EventDetails import get_event, getResultTemplate, saveResult, getResult, submitFeedback, getAllFeedback, getUserRole, uploadImage,getQrCode
app.route('/getResultTemplate', methods=['GET'])(getResultTemplate)
app.route('/saveResult', methods=['POST'])(saveResult)
app.route('/getResult', methods=['GET'])(getResult)
app.route('/getUserRole', methods=['GET'])(getUserRole)
app.route('/submitFeedback', methods=['POST'])(submitFeedback)
app.route('/getAllFeedback', methods=['GET'])(getAllFeedback)
app.route("/getEventDetails", methods=["POST"])(get_event)
app.route("/uploadImage", methods=["POST"])(uploadImage)
app.route("/getQrCode", methods=["GET"])(getQrCode)
# CommentGet
from Model.CommentGet import getComment
app.route("/getcomments", methods=["GET"])(getComment)
# CommentSave
from Model.CommentSave import add_comment, answer_comment
app.route("/addcomment", methods=["POST"])(add_comment)
app.route("/answercomment", methods=["POST"])(answer_comment)
# UpdateNotification
from Model.EventNotification import getNotificationTemplate, saveNotification, getNotification
app.route("/updateNotification", methods=["POST"])(saveNotification)
app.route("/getNotificationTemplate", methods=["GET"])(getNotificationTemplate)
app.route("/getNotification", methods=["GET"])(getNotification)
app.route("/acceptEventApply", methods=["POST"])(acceptEventApply)
app.route("/refuseEventApply", methods=["POST"])(refuseEventApply)
app.route("/acceptInvite", methods=["POST"])(acceptInvite)
app.route("/refuseInvite", methods=["POST"])(refuseInvite)
app.route("/getValidationNotifications", methods=["GET"])(getValidationNotifications)
#class
from Model.ClassAbout import get_class_list, get_class_students, add_student_to_class, remove_student_from_class
app.route("/getClassList", methods=["GET"])(get_class_list)
app.route("/getClassStudents", methods=["GET"])(get_class_students)
app.route("/addStudentToClass", methods=["POST"])(add_student_to_class)
app.route("/removeStudentFromClass", methods=["POST"])(remove_student_from_class)

# @socketio.on("message")
# def handle_message(msg):
#     print("Message: " + msg)
#     send(msg, broadcast=True)


if __name__ == "__main__":
    # socketio.run(app, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True)
    app.run(debug=True)

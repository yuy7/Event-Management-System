from flask import jsonify, request, session
from Dao.Event import Event
from Dao.Location import Location
from Dao.UserAddEvent import UserAddEvent
from Dao.TimeSlot import TimeSlot
from Dao.User import User
from Dao.RoleApply import RoleApply
from Tool.Mappings import building_index2str
from __init__ import db
from datetime import datetime
from Tool.GetUserAllEvent import getUserAllEventByUserID
from Tool.Mappings import role_event_type, event_type_mapping, event_type_str2index

def getLocationList():
    buildings = db.session.query(Location.building).distinct()
    building_info_list = []

    for building_tuple in buildings:
        building_index = building_tuple[0]
        building_str = building_index2str.get(building_index, "未知建筑")
        numbers = Location.query.filter_by(building=building_index).all()
        number_list = [n.number for n in numbers]
        building_info_list.append({"building": building_str, "numbers": number_list})

    return jsonify({"data": building_info_list})

def getEventTypeList():
    # data = request.get_json()
    # userID = data.get("userid")
    userID = request.args.get("userid")
    print(userID)
    user = User.query.filter_by(UserID=userID).first()
    roleApply = RoleApply.query.filter_by(userID=userID).first()
    role =  user.Role if roleApply == None else "学生"
    type_id_list = role_event_type[role]
    event_type_list = [event_type_mapping[id] for id in type_id_list]
    return jsonify({"data": event_type_list})

def EventCreate():
    # user_id = session.get("userID")
    # user_id = 251101164
    data = request.get_json()
    userID = data.get("userid")
    eventName = data.get("name")
    date = data.get("date")
    eventTypeID = event_type_str2index[data.get("eventTypeID")]
    numberOfPeople = data.get("numberOfPeople")
    preferredLocation = data.get("preferredLocation")
    requireApproval = data.get("requireApproval")
    preferredClassroom = data.get("preferredClassroom")
    time = data.get("time")
    preferredLocation = preferredLocation + str(preferredClassroom)
    
    # 判断日期是否合法
    today_str = datetime.now().strftime('%Y-%m-%d')
    if (today_str > date):
        return jsonify({
            "status": "Fail",
            "message": "日期不合法"
        })
    
    event_list = getUserAllEventByUserID(userID)
    for event in event_list:
        time_slot = db.session.query(TimeSlot.timeID).filter(TimeSlot.timeDescription == event['time']).first()
        if time_slot:
            timeID = int(time_slot.timeID)
        else:
            timeID = None  # 或者处理没有找到对应 timeID 的情况
            
        if event['date'] == date and timeID == int(time):
            return jsonify({
                'status': 'Error',
                'message': '时间冲突,冲突的活动名称为'+event['eventName']+'，请重新选择时间'
            }), 409
            


    # 创建新活动并保存到数据库
    newEvent = Event(
        eventName=eventName,
        date=date,
        reservationUserId=userID,
        eventTypeID=eventTypeID,
        numberOfPeople=numberOfPeople,
        preferredLocation=preferredLocation,
        requireApproval=requireApproval,
        time=time
    )
    db.session.add(newEvent)
    db.session.commit()
    return jsonify({
        "status": "Success",
        "message": "创建成功"
    })


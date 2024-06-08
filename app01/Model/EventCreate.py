from flask import jsonify, request, session
from Dao.Event import Event
from Dao.Location import Location
from Dao.UserAddEvent import UserAddEvent
from Dao.TimeSlot import TimeSlot
from Tool.Mappings import building_index2str
from __init__ import db
from datetime import datetime
from Tool.GetUserAllEvent import getUserAllEventByUserID

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

def EventCreate():
    # user_id = session.get("userID")
    # user_id = 251101164
    data = request.get_json()
    userID = data.get("userid")
    eventName = data.get("name")
    date = data.get("date")
    eventTypeID = data.get("eventTypeID")
    numberOfPeople = data.get("numberOfPeople")
    preferredLocation = data.get("preferredLocation")
    requireApproval = data.get("requireApproval")
    time = data.get("time")
    
    
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


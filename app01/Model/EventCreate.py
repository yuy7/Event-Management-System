from flask import jsonify, request, session
from Dao.Event import Event
from Dao.Location import Location
from Tool.Mappings import building_index2str
from __init__ import db

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
    user_id = data.get("userid")
    eventName = data.get("name")
    date = data.get("date")
    eventTypeID = data.get("eventTypeID")
    numberOfPeople = data.get("numberOfPeople")
    preferredLocation = data.get("preferredLocation")
    requireApproval = data.get("requireApproval")
    time = data.get("time")
    
    
    # 创建新活动并保存到数据库
    newEvent = Event(
        eventName=eventName,
        date=date,
        reservationUserId=user_id,
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


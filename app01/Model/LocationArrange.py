from flask import jsonify, request
from datetime import datetime, timedelta
from dateutil import parser
from Dao.Event import Event
from Dao.Role import Role
from Dao.Location import Location
from Dao.User import User
from Tool.OccupyMatrix import is_occupied, get_building_and_number, hex2matric, matric2hex
from Tool.TimeCount import count_days_distance
from __init__ import db
from itertools import chain
from Tool.Mappings import time_mapping, role_mapping, event_type_mapping

def get_user_role(user_id):
    role = Role.query.filter_by(roleName=user_id).first()
    return role_mapping[role.roleName] if role else None


def eventArrange(days_distance, event_list):
    # roleNameList = [get_user_role(event.reservationUserId) for event in event_list]
    # 遍历所有event，如果当前preferredLocation在当天的time时间段为空，则将event、preferredLocation、time加入arrange_list
    # 这个字典将用来存储已安排的事件信息，键为日期和时间的组合，值为Event对象

    # 安排事件
    scheduled_events = {}
    unscheduled_events = []  # 用来追踪未能安排的事件

    for event in event_list:
        key = "{}_{}".format(event.time, event.preferredLocation)
        # 判断在数据库表中该时间该地点是否被占用
        if is_occupied(days_distance, event.time, event.preferredLocation):
            pass
        if key in scheduled_events:
            existing_event = scheduled_events[key]
            # eventTypeID 越小, role 数值越小, 优先级越高。
            existing_event_role = get_user_role(existing_event.reservationUserId)
            new_event_role = get_user_role(event.reservationUserId)
            if (event.eventTypeID < existing_event.eventTypeID or
            (event.eventTypeID == existing_event.eventTypeID and new_event_role < existing_event_role) or
            (event.eventTypeID == existing_event.eventTypeID and new_event_role == existing_event_role and event.eventID < existing_event.eventID)):
                # 替换优先级低的事件
                scheduled_events[key] = event  
            else:
                # 记录未能安排的事件
                unscheduled_events.append(event)
        else:
            # 如果当前时间段此地点为空，则安排当前事件
            scheduled_events[key] = event

    # 准备结果列表，包含活动对象和他们的地点
    result_list = []

    # 将安排的事件添加到结果列表中
    for event in scheduled_events.values():
        result_list.append((event, event.preferredLocation))

    # 将未能安排的事件也添加到结果列表，但他们的地点为 None
    for event in unscheduled_events:
        result_list.append((event, None))
    print(result_list)
    
    return result_list

def locationArrange():
    data = request.get_json()  # 获取JSON数据
    startDateString = data.get('startDate')
    endDateString = data.get('endDate')
    
    # 将日期字符串转换为datetime对象
    try:
        startDate = parser.isoparse(startDateString)
        endDate = parser.isoparse(endDateString)
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    # 判断时间是否有效
    # 是否是未来的一个月内
    now = datetime.now()
    if endDate < startDate:
        return jsonify({'error': 'End date is before start date'}), 400
    if startDate < now or startDate > now + timedelta(days=30):
        return jsonify({'error': 'Start date is not within the next 30 days'}), 400

    arrangeEvents = []  # 假设这是我们要返回的最终列表
    current_date = startDate
    while current_date <= endDate:
        # 转换日期的格式至'yyyy-mm-dd'
        current_date_string = str(current_date.date())
        # print(current_date_string)
        # 添加逻辑来获取每一天的事件
        events = Event.query.filter_by(date=current_date_string).all()
        if events is not None:
            days_distance = count_days_distance(current_date, now)
            result_list = eventArrange(days_distance, events)
            arrangeEvents = list(chain(arrangeEvents, result_list))
        current_date += timedelta(days=1)  # 移至下一天
    
    # 遍历列表中的每个元组
    row1 = 1
    row2 = 1
    for event_tuple in arrangeEvents:
        event_obj, location_name = event_tuple  # 解包元组，获取Event对象和位置信息
            
        # 如果位置信息不是None，则更新Event对象的arrangeLocation属性
        if location_name is not None:
            # 假设Event对象有一个方法set_location，你也可能需要替换这一行以适应你的类设计
            row1 &= Event.query.filter_by(eventID = event_obj.eventID).update({"arrangedLocation":location_name})
            building, number = get_building_and_number(location_name)
            location_obj = Location.query.filter_by(building=building, number=number).first()
            matric = hex2matric(location_obj.occupy)
            matric[days_distance][event_obj.time] = 1
            row2 &= Location.query.filter_by(locationId = location_obj.locationId).update({"occupy":matric2hex(matric)})
    try:
        db.session.commit()
        if(row1 & row2):
            return jsonify({
                "status": "Success"
            })
        elif (row1 == 0):
            raise Exception("Update eventList error!")
        else:
            return Exception("Update Location occupy status error!")
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "Error",
            "message": str(e)
        }), 500

def getArrangedEvents():
    arranged_events = Event.query.filter(Event.arrangedLocation != None).all()
    return jsonify([{
        'eventID': event.eventID,
        'eventName': event.eventName,
        'time': event.date+' '+time_mapping[event.time], 
        'reservationUserName': User.query.filter_by(UserID=event.reservationUserId).first().Username,
        'reservationUserRole': Role.query.filter_by(roleID=event.reservationUserId).first().roleName,
        'arrangedLocation': event.arrangedLocation,
        'eventType': event_type_mapping[event.eventTypeID],
        'numberOfPeople': event.numberOfPeople
    } for event in arranged_events])

def getUnarrangedEvents():
    unarranged_events = Event.query.filter(Event.arrangedLocation == None).all()
    return jsonify([{
        'eventID': event.eventID,
        'eventName': event.eventName,
        'time': event.date+' '+time_mapping[event.time],  
        'reservationUserName': User.query.filter_by(UserID=event.reservationUserId).first().Username,
        'reservationUserRole': Role.query.filter_by(roleID=event.reservationUserId).first().roleName,
        'prefferedLocation': event.preferredLocation,
        'eventType': event_type_mapping[event.eventTypeID],
        'numberOfPeople': event.numberOfPeople
    } for event in unarranged_events])


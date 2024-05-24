from flask import jsonify, request
from datetime import datetime, timedelta
from dateutil import parser
from Dao.TempEvent import Event
from Dao.Role import Role
from Tool.HexMatricTranslate import hex2matrix

role_mapping = {
    "教师":0,
    "辅导员":1,
    "班长":2,
    "社团负责人":3,
    "学生":4
}

def get_user_role(user_id):
    role = Role.query.filter_by(userID=user_id).first()
    return role_mapping[role.roleName] if role else None

def eventArrange(event_list):
    # roleNameList = [get_user_role(event.reservationUserId) for event in event_list]
    # 遍历所有event，如果当前preferredLocation在当天的time时间段为空，则将event、preferredLocation、time加入arrange_list
    # 这个字典将用来存储已安排的事件信息，键为日期和时间的组合，值为Event对象

    # 安排事件
    scheduled_events = {}
    unscheduled_events = []  # 用来追踪未能安排的事件

    for event in event_list:
        key = "{}_{}".format(event.time, event.preferredLocation)
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

    days_data = []  # 用于存储每日的安排
    arrangeEvents = []  # 假设这是我们要返回的最终列表
    current_date = startDate
    while current_date <= endDate:
        # 转换日期的格式至'yyyy-mm-dd'
        current_date_string = str(current_date.date())
        print(current_date_string)
        # 添加逻辑来获取每一天的事件
        events = Event.query.filter_by(date=current_date_string).all()
        eventArrange(events)
        # 为了简化示例，我们这里直接将日期添加至列表
        current_date += timedelta(days=1)  # 移至下一天
        
    return jsonify({
        'status': 'success'
    }), 200

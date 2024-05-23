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
    scheduled_events = {}
    for event in event_list:
        key = "{}_{}".format(event.time, event.preferredLocation)
        
        # 检查此时间和地点是否已有安排的事件
        if key in scheduled_events:
            existing_event = scheduled_events[key]
            
            # 检查当前事件的优先级是否高于已安排的事件
            # eventTypeID越小，优先级越高
            # role越小，优先级越高
            # 如果都一样，按照id，即早预约的占有
            if(event.eventTypeID < existing_event.eventTypeID or
               (event.eventTypeID < existing_event.eventTypeID and 
                get_user_role(event.reservationUserId) < get_user_role(existing_event.eventTypeID))):
                # 替换低优先级的事件，以当前事件占位
                scheduled_events[key] = event
            if event.priority > existing_event.priority:
                # 替换低优先级的事件，以当前事件占位
                scheduled_events[key] = event                
            # 若优先级不足以替换，当前事件不安排
        else:
            # 如果当前时间段此地点为空，则安排当前事件
            scheduled_events[key] = event
    
    
    return arrange_list
    
    pass

def arrange_event(event_list):
    arrange_list = []

    for event in event_list:
        key = "{}_{}_{}".format(event.date, event.time, event.preferredLocation)
        
        # 检查此时间和地点是否已有安排的事件
        if key in scheduled_events:
            existing_event = scheduled_events[key]
            
            # 检查当前事件的优先级是否高于已安排的事件
            if event.priority > existing_event.priority:
                # 替换低优先级的事件，以当前事件占位
                scheduled_events[key] = event
                arrange_list.append((event.eventID, event.preferredLocation, event.time))
                
                # 此处可以添加逻辑处理被替换掉的事件，例如重新安排
            # 若优先级不足以替换，当前事件不安排
        else:
            # 如果当前时间段此地点为空，则安排当前事件
            scheduled_events[key] = event
            arrange_list.append((event.eventID, event.preferredLocation, event.time))
    
    return arrange_list


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

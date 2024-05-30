# from datetime import datetime
# from Dao.UserEvent import UserEvent
# from  Dao.Event import Event
# from flask import session
# from sqlalchemy import or_, and_, not_

# def getHistoryEvents():
#     # userID = session.get("userid")  # 从session中获取userID
#     userID = 251101163
#     now = datetime.now().strftime('%Y-%m-%d')  # 获取当前日期，并转化为字符串格式YYYY-MM-DD

#     # 查询用户过去参加过的活动
#     attended_events = Event.query.join(UserEvent, Event.eventID == UserEvent.eventID)\
#                                  .filter(UserEvent.userID == userID,
#                                          Event.date < now).all()

#     # 查询用户过去预约过的活动
#     # reserved_events = Event.query.filter(and_(Event.reservationUserId=userID,
#     #                                         Event.date < now)).all()

#     # 合并两个列表，并去重（假定一个事件不可能同时在两个列表中）
#     all_history_events = list({event.eventID: event for event in attended_events}.values())

#     return all_history_events
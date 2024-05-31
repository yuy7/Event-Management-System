import copy
from Tool.OccupyMatrix import matrix2hex, hex2matrix
from Tool.TimeCount import count_days_distance
from Dao.Location import Location
from Dao.Update import Update
from datetime import datetime
from __init__ import db

def matrix_shift(matrix, days):
    new_matrix = matrix
    days = 30 if days>30 else days
    if days < 30:
        new_matrix[:-days] = copy.deepcopy(matrix[days:])
    for row in range(30-days, 30, 1):  # 这里的2表示前两行
        for col in range(len(matrix[row])):
            new_matrix[row][col] = 0
    return new_matrix

def update_db():
    last_login = Update.query.order_by(Update.UpdateID.desc()).first()
    days = 0
    now = datetime.now()
    if last_login is None:
        # 第一次登录
        days = 30
    else:
        days = count_days_distance(now, last_login.LastLoginTime)
    pass
    locationList = Location.query.all()
    flag = 1
    for location in locationList:
        location = Location.query.filter_by(locationId=location.locationId).first()
        matrix = hex2matrix(location.occupy)
        new_matrix = matrix_shift(matrix, days)
        flag &= Location.query.filter_by(locationId=location.locationId).update({"occupy":matrix2hex(new_matrix)})
    num_deleted = db.session.query(Update).delete()
    new_record = Update(LastLoginTime=datetime.now())
    db.session.add(new_record)

    if flag == 1:
        try:
            db.session.commit()
            if(flag):
                return "Success"
            elif (flag == 0):
                raise Exception("Update Location Matrix Error!")
            else:
                return Exception("Update Location Db Error!")
        except Exception as e:
            db.session.rollback()
            return str(e)
            
import copy
from Tool.OccupyMatrix import matric2hex, hex2matric
from Dao.Location import Location
def matrix_shift(matrix, days):
    new_matrix = matrix
    days = 30 if days>30 else days
    if days < 30:
        new_matrix[:-days] = copy.deepcopy(matrix[days:])
    for row in range(30-days, 30, 1):  # 这里的2表示前两行
        print(row)
        for col in range(len(matrix[row])):
            new_matrix[row][col] = 0
            print(str(row)+','+str(col))
            print(new_matrix)
    print(new_matrix)
    return new_matrix

def update_db():
    pass
    # locationList = Location.query.all()
    # flag = 1
    # for location in locationList:
        
    pass
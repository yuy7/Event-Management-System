# 如果没有比自己优先级更高的人，则能在选择的偏好时间段预约到偏好的教室
# 如果有，则


# 人员优先级：
# 教师 / 辅导员 / 班长 / 社团/部门负责人 / 学生

# 大型考试——四六级考试或考研（抢占式）
# 教务员：考试周考试（抢占式）
# 重要的宣讲（优先级较高）
# 老师：授课、考试（符合人数要求）、个人活动
# 辅导员：年级会、个人活动
# 班长：班级会、个人活动
# 社团/部门负责人：社团 / 部门活动
# 学生：个人活动

# event_mapping = {
#     0:"大型考试",
#     1:"统一考试",
#     2:"宣讲",
#     3:"授课",
#     4:"课程考试",
#     5:"开会",
#     6:"学生活动",
#     7:"其他"
# }
# from Dao.TempEvent import Event
# startDate = '2024-05-27'
# events = Event.query.filter_by(date=startDate).all()
# print(events)

# building_mapping = {
#     "逸夫楼": 0,
#     "机电楼": 1,
#     "教学楼": 2
# }

# print(building_mapping["逸夫楼"])
# 示例十六进制字符串的转换

def hex2matric(hex_string):
    # 将十六进制字符串转换为二进制字符串，去除前缀'0b'并确保位数为184
    binary_string = bin(int(hex_string, 16))[2:].zfill(184)

    # 确保前4位为0，如果不为0，说明数据格式可能存在错误
    if binary_string[:4] != '0000':
        raise ValueError("Input hex string is not in the expected format")
    
    # 提取用于表示矩阵的180位
    binary_string = binary_string[4:]

    matric = []
    for i in range(30):  # 对每一天
        row = []
        for j in range(6):  # 对每个时间段
            # 计算当前时间段在二进制字符串中的位置
            index = i * 6 + j
            # 将这一位的值添加到当天的占用情况列表中
            row.append(int(binary_string[index]))
        # 将当天的占用情况添加到整个月的矩阵中
        matric.append(row)
        
    return matric

def matric2hex(matric):
    if len(matric) != 30 or any(len(row) != 6 for row in matric):
        raise ValueError("Input matric must be 30x6 size")

    # 开始构建二进制字符串，先添加4个前导0
    binary_string = '0000'

    # 遍历30x6的矩阵，并将1或0添加到二进制字符串中
    for row in matric:
        for value in row:
            if value not in [0, 1]:
                raise ValueError("matric values must be 0 or 1 only")
            binary_string += str(value)

    # 确保二进制字符串长度正好为184位
    if len(binary_string) != 184:
        raise ValueError("The binary string representation must be of length 184")

    # 将二进制字符串转换为十六进制表示，并去掉前缀'0x'
    hex_string = hex(int(binary_string, 2))[2:].upper()

    # zfill用于在字符串前面填充0直到有46个字符，因为16进制数每个字符代表4位二进制数
    hex_string = hex_string.zfill(45)

    return hex_string

hex_string = '0300FFFFFFFFFFFFFFFFFFF0300FFFFFFFFFFFFFFFFFF'  # 示例十六进制字符串
print(hex_string)
matric = hex2matric(hex_string)
# 打印转换后的矩阵
for row in matric:
    print(row)
hex = matric2hex(matric)
print(hex)
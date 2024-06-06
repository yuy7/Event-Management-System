from Dao.Location import Location
from Tool.Mappings import building_mapping

def hex2matrix(hex_string):
    # 将十六进制字符串转换为二进制字符串，去除前缀'0b'并确保位数为184
    binary_string = bin(int(hex_string, 16))[2:].zfill(184)

    # 确保前4位为0，如果不为0，说明数据格式可能存在错误
    if binary_string[:4] != '0000':
        raise ValueError("Input hex string is not in the expected format")
    
    # 提取用于表示矩阵的180位
    binary_string = binary_string[4:]

    matrix = []
    for i in range(30):  # 对每一天
        row = []
        for j in range(6):  # 对每个时间段
            # 计算当前时间段在二进制字符串中的位置
            index = i * 6 + j
            # 将这一位的值添加到当天的占用情况列表中
            row.append(int(binary_string[index]))
        # 将当天的占用情况添加到整个月的矩阵中
        matrix.append(row)
        
    return matrix

def matrix2hex(matrix):
    if len(matrix) != 30 or any(len(row) != 6 for row in matrix):
        raise ValueError("Input matrix must be 30x6 size")

    # 开始构建二进制字符串，先添加4个前导0
    binary_string = '0000'

    # 遍历30x6的矩阵，并将1或0添加到二进制字符串中
    for row in matrix:
        for value in row:
            if value not in [0, 1]:
                raise ValueError("matrix values must be 0 or 1 only")
            binary_string += str(value)

    # 确保二进制字符串长度正好为184位
    if len(binary_string) != 184:
        raise ValueError("The binary string representation must be of length 184")

    # 将二进制字符串转换为十六进制表示，并去掉前缀'0x'
    hex_string = hex(int(binary_string, 2))[2:].upper()

    # zfill用于在字符串前面填充0直到有46个字符，因为16进制数每个字符代表4位二进制数
    hex_string = hex_string.zfill(45)

    return hex_string

def get_building_and_number(location_name):
    import re
    # Use regex to match characters and numbers
    matches = re.match(r'(\D+)(\d+)', location_name)

    if matches:
        building_string, number = matches.groups()
        building = building_mapping[building_string]
        
    return building, number


def is_occupied(days_distance, time, location_name):
    building, number = get_building_and_number(location_name)
    location = Location.query.filter_by(building=building, number=number).first()
    matrix = hex2matrix(location.occupy)
    return matrix[days_distance][time]

# 示例十六进制字符串的转换
# hex_string = '0300FFFFFFFFFFFFFFFFFFF0300FFFFFFFFFFFFFFFFFF'  # 示例十六进制字符串
# matrix = hex2matrix(hex_string)
# 打印转换后的矩阵
# for row in matrix:
#     print(row)





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

# 示例十六进制字符串的转换
# hex_string = '0300FFFFFFFFFFFFFFFFFFF0300FFFFFFFFFFFFFFFFFF'  # 示例十六进制字符串
# matrix = hex2matrix(hex_string)
# 打印转换后的矩阵
# for row in matrix:
#     print(row)




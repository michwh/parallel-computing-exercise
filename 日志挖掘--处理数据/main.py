# coding = utf-8

import ast
import time

# 将两条数据整理成一条车次信息
def organizeData(msg1, msg2):
    result = {
        'number': msg1[2],
        'in_time': msg1[0],
        'out_time': msg2[0]
    }
    return result

# 加载数据，将整理后的数据写入result.txt文件
def loadDataSet():
    message = []
    with open("cars.txt", "r") as f:
        line1 = f.readline()
        line2 = f.readline()
        while line1:
            msg1 = line1.split(',')
            msg2 = line2.split(',')
            if msg1[1] == '201616100313':
                result = organizeData(msg1, msg2)
                message.append(result)
            line1 = f.readline()
            line2 = f.readline()
    f.close()

    with open("result.txt", "w") as f:
        for msg in message:
            f.write(str(msg)+'\n')
    f.close()

# 将时间转成时间戳，并计算时间差
def processingTime(in_time, out_time):
    in_time = time.mktime(time.strptime(in_time, '%Y-%m-%d %H:%M:%S'))
    out_time = time.mktime(time.strptime(out_time, '%Y-%m-%d %H:%M:%S'))
    return out_time - in_time


# 统计数据
def statisticalData(fileName):
    resultNumber = 0
    resultTime = 0
    with open(fileName, "r") as f:
        for line in f:
            resultNumber += 1
            line = ast.literal_eval(line.strip('\n'))
            resultTime += processingTime(line['in_time'], line['out_time'])
    f.close()
    return resultNumber, resultTime

def main():
    loadDataSet()
    resultNumber, resultTime = statisticalData("result.txt")
    print(resultNumber)
    print(resultTime)

if __name__ == "__main__":
    main()
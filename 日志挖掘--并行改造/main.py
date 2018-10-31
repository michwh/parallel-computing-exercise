# coding = utf-8

import ast
import time
import datetime
import threading

# 总车次数
resultNumber = 0

# 累计停放时间
resultTime = 0

# 线程锁
lock = threading.Lock()


def organizeData(msg1, msg2):
    """将两条数据整理成一条车次信息

    :param msg1: 车辆进入停车场的信息
    :param msg2: 车辆离开停车场的信息
    :return result: 整理后的车次信息
    """
    result = {
        'number': msg1[2],
        'in_time': msg1[0],
        'out_time': msg2[0]
    }
    return result


def writeFileByDate(dateDict):

    """根据入场日期将车次信息写入不同的文件

    :param dateDict: 根据车辆进入停车场时间划分好的字典数据
    :return:
    """
    for key, value in dateDict.items():
        with open("result/" + key + ".txt", "w") as f:
            for k in value:
                f.write(str(k) + '\n')
        f.close()


def loadDataSet():
    """加载数据，整理数据

    :return:
    """
    dateDict = {}
    dateList = []
    with open("cars.txt", "r") as f:
        line1 = f.readline()
        line2 = f.readline()
        while line1:
            msg1 = line1.split(',')
            msg2 = line2.split(',')
            if msg1[1] == '201616100313':

                # 将车辆进出信息整理成一条车次信息
                result = organizeData(msg1, msg2)

                # 将车次信息按照进入时间进行分类
                inDate = result['in_time'][0:10]
                if inDate in dateDict:
                    dateDict[inDate].append(result)
                else:
                    dateDict[inDate] = []
                    dateDict[inDate].append(result)
                    dateList.append(inDate)

            line1 = f.readline()
            line2 = f.readline()
    f.close()

    return dateList, dateDict


def processingTime(in_time, out_time):
    """将时间转成时间戳，并计算时间差

    :param in_time: 车辆进入停车场的时间
    :param out_time: 车辆离开停车场的时间
    :return: 时间差
    """
    in_time = time.mktime(time.strptime(in_time, '%Y-%m-%d %H:%M:%S'))
    out_time = time.mktime(time.strptime(out_time, '%Y-%m-%d %H:%M:%S'))
    return out_time - in_time


def statisticalData(th, threadCount, dateList):
    """统计数据

    :param th: 第几个线程
    :param threadCount: 线程总数
    :param dateList: 车辆进入停车场时间的列表
    :return:
    """
    global resultNumber, resultTime

    count = th
    while count < len(dateList):
        with open("result/" + dateList[count] + ".txt", "r") as f:
            message = f.readlines()
        f.close()
        for line in message:
            # 将字符串转成字典
            line = ast.literal_eval(line.strip('\n'))

            # 对线程进行锁定，防止资源冲突
            lock.acquire()

            resultNumber += 1
            resultTime += processingTime(line['in_time'], line['out_time'])

            # 释放锁
            lock.release()
        count += threadCount


def createThread(threadCount, dateList):
    """创建多线程

    :param threadCount: 需创建的线程数
    :param dateList: 车辆进入停车场时间的列表
    :return threads: 线程列表
    """
    threads = []
    for i in range(threadCount):
        try:
            threads.append(threading.Thread(target=statisticalData, args=(i, threadCount, dateList)))
        except:
            print('无法启动线程')
    for t in range(len(threads)):
        threads[t].start()
    return threads


def main():
    # 读取数据
    print('Start ReadFile:00:00:00.000')
    startTime = time.perf_counter()
    dateList, dateDict = loadDataSet()
    readFileTime = time.perf_counter()

    # 输出读取日志的时间
    seconds = readFileTime - startTime
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    print('End ReadFile:%d:%02d:%.3f' % (h, m, s))

    # 根据分类结果写入不同的文件
    writeFileByDate(dateDict)

    # 创建线程
    threadCount = 1
    threads = createThread(threadCount, dateList)

    # 等待所有的线程结束，再执行下面的操作
    for i in range(threadCount):
        threads[i].join()

    # 输出整个程序运行的时间
    endProcessTime = time.perf_counter()
    seconds = endProcessTime - startTime
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    print('End Process:%d:%02d:%.3f' % (h, m, s))

    # 输出结果
    print('线程数：', threadCount)
    print('总车次数：', resultNumber)
    print('总停放时间：', resultTime, 's')


if __name__ == "__main__":
    main()

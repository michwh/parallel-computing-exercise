import random
import copy
import time
import threading

# 棋盘的行列数
row = 100
column = 100

# 进化代数
count = 50

nCellSta = [[random.randint(0, 1) for i in range(column)] for j in range(row)]
nTempSta = [[0 for p in range(column)] for q in range(row)]


def CellCount(nRow, nColumn):
    global row, column, nCellSta
    nSum = 0
    for i in range(nRow - 1, nRow + 2):
        for j in range(nColumn - 1, nColumn + 2):
            if i < 0 or i > row - 1 or j < 0 or j > column - 1 or i == nRow and j == nColumn:
                continue
            if nCellSta[i][j] == 1:
                nSum += 1
    if nSum == 0 or nSum == 1 or nSum == 4 or nSum == 5 or nSum == 6 or nSum == 7 or nSum == 8:
        return 0
    elif nSum == 2:
        return nCellSta[nRow][nColumn]
    elif nSum == 3:
        return 1


# 对一整行的细胞进行计算
def rowCellCount(i):
    for j in range(column):
        nTempSta[i][j] = CellCount(i, j)


# 输出列表nCellSta的值
def printValue():
    nSum = 0
    global row, column
    for i in range(row):
        for j in range(column):
            # print(nCellSta[i][j], ' ', end='')
            nSum += nCellSta[i][j]
        # print('\n')
    return nSum


def createThread(threadCount):
    """创建多线程
    :param threadCount: 需创建的线程数
    :param dateList: 车辆进入停车场时间的列表
    :return threads: 线程列表
    """
    threads = []
    for i in range(threadCount):
        try:
            threads.append(threading.Thread(target=rowCellCount, args=(i, threadCount)))
        except:
            print('无法启动线程')
    for t in range(len(threads)):
        threads[t].start()
    return threads


def main():
    global count, nCellSta, nTempSta
    printValue()
    startTime = time.perf_counter()
    for k in range(count - 1):
        # print('新一轮游戏：\n')
        for i in range(row):

        nCellSta = copy.deepcopy(nTempSta)
        if not printValue():
            print('全部死亡，进化结束')
            break

    endTime = time.perf_counter()
    seconds = endTime - startTime
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    print('花费时间为：%d:%02d:%.3f' % (h, m, s))


if __name__ == "__main__":
    main()

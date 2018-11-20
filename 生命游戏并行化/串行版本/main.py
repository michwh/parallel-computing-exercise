import random
import copy
import time
import gc

# 棋盘的行列数
row = 50
column = 50

# 进化代数
count = 10

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


# 输出列表nCellSta的值
def printValue():
    nSum = 0
    global row, column, nCellSta
    for i in range(row):
        for j in range(column):
            # 打印效果
            # print(nCellSta[i][j], ' ', end='')
            nSum += nCellSta[i][j]
        # print('\n')
    return nSum


def main():
    global count, nCellSta, nTempSta
    # printValue()
    startTime = time.perf_counter()
    for k in range(count - 1):
        # print('新一轮游戏：\n')
        # nTempSta = [[0 for p in range(column)] for q in range(row)]
        # nTempSta = [0 for p in range(column)]
        for i in range(row):
            for j in range(column):
                nTempSta[i][j] = CellCount(i, j)
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

# coding: utf8

import threading
import time

pi = 0

# 各线程调用的方法
def solve(f, interval, accuracy):
    '''

    :param f:开始计算的项
    :param interval:项数间隔
    :param accuracy:计算的精度
    :return:
    '''
    sign = 1 if (f - 1) / 2 % 2 == 0 else -1
    i = sign / f
    result = 0
    interval *= 2
    while abs(i) >= accuracy:  # 精度控制
        result += i
        f += interval
        sign = 1 if (f - 1) / 2 % 2 == 0 else -1
        i = sign / f
    global pi
    pi += result

# 创建多线程
def createThread(threadCount, accuracy):
    '''

    :param threadCount: 线程数
    :param accuracy: 计算精度
    :return threads: 线程集合
    '''
    threads = []
    for i in range(threadCount):
        try:
            threads.append(threading.Thread(target=solve, args=(2 * i + 1, threadCount, accuracy)))
        except:
            print('无法启动线程')
    for t in range(len(threads)):
        threads[t].start()
    return threads

# 获得最后的结果
def getResult(threadCount):
    '''

    :param threadCount: 线程数
    :return pi: 所求得的PI值
    '''
    global pi
    pi = 0
    threads = createThread(threadCount, 1e-6)
    for i in range(threadCount):
        threads[i].join()
    pi *= 4
    return pi

def main():

    print('\n单线程：')
    start_time = time.process_time()
    result = getResult(1)
    print('PI = ' + str(result))
    end_time = time.process_time()
    print('单线程时间：%.3f [s]' % (end_time - start_time))

    print('\n2线程：')
    start_time = time.process_time()
    result = getResult(2)
    print('PI = ' + str(result))
    end_time = time.process_time()
    print('2线程时间：%.3f [s]' % (end_time - start_time))

    print('\n4线程：')
    start_time = time.process_time()
    result = getResult(4)
    print('PI = ' + str(result))
    end_time = time.process_time()
    print('4线程时间：%.3f [s]' % (end_time - start_time))



if __name__ == "__main__":
    main()

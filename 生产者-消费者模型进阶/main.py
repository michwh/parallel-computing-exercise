import threading
import random
import time
import queue
import math
import multiprocessing
from consumer import Consumer
from producer import Producer
from queueService import ThreadPoolManger


def main():
    startTime = time.perf_counter()

    # 用于存放随机数的队列
    q = queue.Queue()

    # 创建缓存进程
    thread_pool = multiprocessing.Process(target=ThreadPoolManger, args=(4,))
    thread_pool.start()

    # 创建生产者进程
    p = multiprocessing.Process(target=Producer, args=(q, thread_pool))
    p.start()

    # 创建消费者进程
    c = multiprocessing.Process(target=Consumer, args=(q, thread_pool))
    c.start()

    endTime = time.perf_counter()
    seconds = endTime - startTime
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    print('程序运行花费时间：%d:%02d:%.3f' % (h, m, s))


if __name__ == '__main__':
    main()

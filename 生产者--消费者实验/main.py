import threading
import random
import time
import queue
import math

# queue = queue.Queue()


class Producer(threading.Thread):
    def __init__(self, producerNum, q):
        threading.Thread.__init__(self)
        self.producerNum = producerNum
        self.data = q

    def run(self):
        for i in range(int(1e6 / self.producerNum)):
            num = random.randint(5e9, 2**63 - 2)
            # num = random.randint(10, 100)
            # print('插入', num)
            self.data.put(num)


class Consumer(threading.Thread):
    def __init__(self, q):
        threading.Thread.__init__(self)
        self.data = q

    # def run(self):
    #     while not self.data.empty():
    #         num = self.data.get()
    #         # 质数大于 1
    #         if num > 1:
    #             # 查看因子
    #             for i in range(2, num):
    #                 if (num % i) == 0:
    #                     print(num, "不是质数")
    #                     break
    #             else:
    #                 print(num, "是质数")
    #
    #         # 如果输入的数字小于或等于 1，不是质数
    #         else:
    #             print(num, "不是质数")

    def run(self, k=5):
        while not self.data.empty():
            flag = 1
            num = self.data.get()
            for i in range(0, k):
                a = random.randint(1, num - 1)
                if pow(a, num - 1, num) != 1:
                    flag = 0
                    print(num, "不是质数")
                    break
            if flag == 0:
                continue
            print(num, "是质数")

    # def run(self):
    #     while not self.data.empty():
    #         flag = 1
    #         num = self.data.get()
    #         for i in range(2, int(math.sqrt(num))):
    #             if (num % i) == 0:
    #                 flag = 0
    #                 print(num, "不是质数")
    #                 break
    #         if flag == 0:
    #             continue
    #         print(num, "是质数")


def main():
    startTime = time.perf_counter()

    # 消费者数量
    consumerNum = 4

    # 生产者数量
    producerNum = 2

    # 生产者线程列表
    producerList = []

    # 消费者线程列表
    consumerList = []

    # 用于存放随机数的队列
    q = queue.Queue()

    for i in range(producerNum):
        p = Producer(producerNum, q)
        p.start()
        producerList.append(p)

    for j in range(consumerNum):
        c = Consumer(q)
        c.start()
        consumerList.append(c)

    for m in range(producerNum):
        producerList[m].join()

    for n in range(consumerNum):
        consumerList[n].join()

    endTime = time.perf_counter()
    seconds = endTime - startTime
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    print('程序运行花费时间：%d:%02d:%.3f' % (h, m, s))


if __name__ == '__main__':
    main()

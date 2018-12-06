import threading
import random
from queueService import QueueService


class Consumer(threading.Thread):
    def __init__(self, q, thread_pool):
        threading.Thread.__init__(self)
        self.data = q
        self.

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


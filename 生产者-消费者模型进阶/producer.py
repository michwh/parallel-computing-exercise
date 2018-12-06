import multiprocessing
import random
from queueService import ThreadPoolManger


class Producer(multiprocessing.Process):
    def __init__(self, q):
        multiprocessing.Process.__init__(self)
        self.data = q

    def run(self):
        for i in range(int(1e6)):
            num = random.randint(5e9, 2**63 - 2)
            self.data.put(num)
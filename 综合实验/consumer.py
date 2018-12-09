import multiprocessing
import socket
import random


class Consumer(multiprocessing.Process):
    def __init__(self):
        multiprocessing.Process.__init__(self)
        # 创建 socket 对象
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 获取本地主机名
        host = socket.gethostname()
        # 设置端口号
        port = 9999
        # 连接服务，指定主机和端口
        self.s.connect((host, port))

    def run(self, k=5):
        # 调用消息队列的方法，0，该进程任务是否完成
        msg = 'get,' + str(0) + ',0'
        self.s.send(msg.encode('utf-8'))
        data = self.s.recv(1024).decode('utf-8').split(',')
        num = int(data[1])
        while not data[0] == '1':
            flag = 1
            for i in range(0, k):
                a = random.randint(1, num - 1)
                if pow(a, num - 1, num) != 1:
                    flag = 0
                    print(num, "不是质数")
                    break
            msg = 'get,' + str(0) + ',0'
            self.s.send(msg.encode('utf-8'))
            data = self.s.recv(1024).decode('utf-8').split(',')
            n = num
            num = int(data[1])
            if flag == 0:
                continue
            print(n, "是质数")
        msg = 'get,' + str(0) + ',1'
        self.s.send(msg.encode('utf-8'))
        # 打印服务端的响应消息
        print(self.s.recv(1024).decode('utf-8'))
        self.s.close()

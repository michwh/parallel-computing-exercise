import multiprocessing
import socket
import random


class Producer(multiprocessing.Process):
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

    def run(self):
        # for i in range(int(1e6)):
        for i in range(10):
            num = random.randint(5e9, 2 ** 63 - 2)
            # 调用消息队列的方法，发送给队列的数字，该进程任务是否完成
            data = 'put,' + str(num) + ',0'
            self.s.send(data.encode('utf-8'))
            # 打印服务端的响应消息
            print(self.s.recv(1024).decode('utf-8'))

        # 向服务端发送消息表示该进程任务完成
        data = 'put,' + str(0) + ',1'
        self.s.send(data.encode('utf-8'))
        # 打印服务端的响应消息
        print(self.s.recv(1024).decode('utf-8'))
        self.s.close()

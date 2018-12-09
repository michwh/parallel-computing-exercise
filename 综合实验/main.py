from producer import Producer
from consumer import Consumer
from threadService import ThreadPoolManger
import queue
import socket
import threading
import sys


# 将数据放入队列，任务完成后向客户端发送响应信息
def put_message(client_socket, data, message_queue):
    # data = client_socket.recv(1024).decode('utf-8').split(',')
    num = data[1]
    message_queue.put(num)
    msg = '已将 %s 放入队列中' % num
    client_socket.send(msg.encode('utf-8'))
    # client_socket.close()


# 将数据从队列中取出，任务完成后向客户端发送响应信息
def get_message(client_socket, message_queue):
    if not message_queue.empty():
        # print('队列不空')
        num = message_queue.get()
        # print('要取数字是' + str(num))
        # 队列是否为空，发送的数字
        msg = str(0) + ',' + str(num)
        client_socket.send(msg.encode('utf-8'))
    else:
        # print('队列空')
        msg = str(1) + ',' + str(0)
        client_socket.send(msg.encode('utf-8'))
        # client_socket.close()


# 处理客户端和服务器之间的通信
def tcp_link(client_socket, addr, thread_pool, message_queue):
    print('接受来自%s:%s的连接' % addr)
    while True:
        data = client_socket.recv(1024).decode('utf-8').split(',')
        # 当该进程任务完成时跳出循环
        if int(data[2]) == 1:
            msg = '来自%s:%s的任务完成' % addr
            client_socket.send(msg.encode('utf-8'))
            break
        if data[0] == 'put':
            thread_pool.add_job(put_message, * (client_socket, data, message_queue))
        elif data[0] == 'get':
            thread_pool.add_job(get_message, * (client_socket, message_queue))
    client_socket.close()


def main():
    # 创建 socket 对象
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 获取本地主机名
    host = socket.gethostname()
    port = 9999
    # 绑定端口号
    server_socket.bind((host, port))
    # 设置最大连接数，超过后排队
    server_socket.listen(5)

    # 线程池队列
    work_queue = queue.Queue()

    # 消息队列
    message_queue = queue.Queue()

    # 创建一个有4个线程的线程池
    thread_pool = ThreadPoolManger(4, work_queue)

    # 启动生产者进程
    p = Producer()
    p.start()

    # 启动消费者进程
    c = Consumer()
    c.start()

    while True:
        # 建立客户端连接
        client_socket, addr = server_socket.accept()
        t = threading.Thread(target=tcp_link, args=(client_socket, addr, thread_pool, message_queue))
        t.start()


if __name__ == '__main__':
    main()

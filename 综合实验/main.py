from producer import Producer
from consumer import Consumer
import socket
import threading
import mns_python_sdk.sample.sendmessage as send_msg
import mns_python_sdk.sample.recvdelmessage as recv_msg


# 将数据放入队列，任务完成后向客户端发送响应信息
def put_message(client_socket, data):
    num = data[1]
    send_msg.my_send_msg(num)
    ms = '已将 %s 放入队列中' % num
    client_socket.send(ms.encode('utf-8'))


# 将数据从队列中取出，任务完成后向客户端发送响应信息
def get_message(client_socket):
    num = recv_msg.my_recv_msg()
    # 队列是否为空，发送的数字
    msg = str(0) + ',' + str(num)
    client_socket.send(msg.encode('utf-8'))


# 处理客户端和服务器之间的通信
def tcp_link(client_socket, addr):
    print('接受来自%s:%s的连接' % addr)
    while True:
        data = client_socket.recv(1024).decode('utf-8').split(',')
        # 当该进程任务完成时跳出循环
        if int(data[2]) == 1:
            msg = '来自%s:%s的任务完成' % addr
            client_socket.send(msg.encode('utf-8'))
            break
        if data[0] == 'put':
            put_message(client_socket, data)
        elif data[0] == 'get':
            get_message(client_socket)
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

    # 启动生产者进程
    p = Producer()
    p.start()

    # 启动消费者进程
    c = Consumer()
    c.start()

    while True:
        # 建立客户端连接
        client_socket, addr = server_socket.accept()
        t = threading.Thread(target=tcp_link, args=(client_socket, addr))
        t.start()


if __name__ == '__main__':
    main()

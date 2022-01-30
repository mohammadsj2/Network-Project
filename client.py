import socket
import threading

host = '127.0.0.1'
port = 8008

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

# TODO Firewall part should be added.
message = input('(shalgham | choghondar) [via port]')
client.send(message.encode('ascii'))


# Init of reading
def read():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            print(message)
        except:
            break


# Init of writing
def write():
    while True:
        message = input()
        try:
            client.send(message.encode('ascii'))
        except:
            client.close()


thread_read = threading.Thread(target=read)
thread_write = threading.Thread(target=write)

thread_read.start()
thread_write.start()

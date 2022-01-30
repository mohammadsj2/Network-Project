import socket
import threading

server_host = '127.0.0.1'
server_port = 8010

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((server_host, server_port))
server.listen(10)


def read_and_write(client: socket.socket):
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            print(f'{message} is received in server ...')
            client.send(f'You have sent us {message} ...'.encode('ascii'))
        except Exception as e:
            print(e)
            break


def run():
    while True:
        client, address = server.accept()
        print(address)
        read_and_write_thread = threading.Thread(target=read_and_write, args=(client,))
        read_and_write_thread.start()


if __name__ == '__main__':
    run()
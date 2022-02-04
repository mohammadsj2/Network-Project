import socket
import threading
from config import *
from tunnel import connect_and_create_tunnel


# TODO: when we close connections in each file? They were sensitive in this matter at the first homework review time

def init_connection(client: socket.socket):
    server_name = client.recv(1024).decode('ascii')
    dest_port = server_to_port[server_name]

    t = connect_and_create_tunnel(client, dest_port)
    tunnels.append(t)


def run():
    while True:
        client, address = server.accept()
        print(address)

        init_thread = threading.Thread(target=init_connection, args=(client,))
        init_thread.start()


if __name__ == '__main__':

    tunnels = []

    while True:
        proxy_port = int(input('Proxy port (put 0 for auto port picking):\n'))
        if proxy_port in INVALID_PORTS:
            print(f"Your port is in our invalid ports please choose another port that is not in {INVALID_PORTS}.")
        else:
            break

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((localhost, proxy_port))
    server.listen(10)
    proxy_port = server.getsockname()[1]

    print(f'your proxy port is: {proxy_port}')
    try:
        run()
    finally:
        server.close()

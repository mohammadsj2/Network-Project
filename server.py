import socket
import threading
from tunnel import Tunnel

server_host = '127.0.0.1'
server_port = 8008

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((server_host, server_port))
server.listen(10)

tunnels = []


def init_connection(client: socket.socket):
    # After connection of client, server expects the servername [via port] to get connected to.
    message = client.recv(1024).decode('ascii')
    parts = message.split(' ')
    server_name = parts[0]

    if len(parts) == 1:
        host = '127.0.0.1'
        chatroom_port = 8009
        streamer_port = 8010
        socket_to_dest_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if server_name == 'chogondar':
            socket_to_dest_server.connect((host, chatroom_port))
        else:
            socket_to_dest_server.connect((host, streamer_port))

        t = Tunnel(first_socket=client, second_socket=socket_to_dest_server)
        t.run()
        tunnels.append(t)

    else:
        proxy_port = int(parts[1])

        host = '127.0.0.1'
        port = proxy_port

        socket_to_proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_to_proxy.connect((host, port))

        # sends which server the client wants to get connected to.
        socket_to_proxy.send(server_name.encode('ascii'))

        t = Tunnel(first_socket=client, second_socket=socket_to_proxy)
        t.run()
        tunnels.append(t)

        # TODO: shall we have a lock so that we can make sure the
        #  connection to the server_name has been established before creating this tunnel?


def run():
    while True:
        client, address = server.accept()
        print(address)
        init_thread = threading.Thread(target=init_connection, args=(client,))
        init_thread.start()


if __name__ == '__main__':
    run()

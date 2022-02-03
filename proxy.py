import socket
import threading
from tunnel import Tunnel

proxy_host = '127.0.0.1'
proxy_port = 8011
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tunnels = []


def init_connection(client: socket.socket):
    server_name = client.recv(1024).decode('ascii')

    # TODO: maybe it is not a bad idea to write these addresses in a file and
    #  write a function to read them from that instead of hardcode.

    host = '127.0.0.1'
    chatroom_port = 8009
    streamer_port = 8010
    socket_to_dest_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if server_name == 'chogondar':
        socket_to_dest_server.connect((host, chatroom_port))
    else:
        socket_to_dest_server.connect((host, streamer_port))

    # TODO: race time! (fixed with dealy in server :D)
    t = Tunnel(first_socket=client, second_socket=socket_to_dest_server)
    t.run()

    tunnels.append(t)



def run():
    while True:
        client, address = server.accept()
        print(address)

        init_thread = threading.Thread(target=init_connection, args=(client,))
        init_thread.start()


if __name__ == '__main__':
    proxy_num = int(input('proxy number '))
    proxy_port = proxy_port + proxy_num

    server.bind((proxy_host, proxy_port))
    server.listen(10)

    run()




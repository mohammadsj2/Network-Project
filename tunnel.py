import socket
import threading
from config import *
from utils import *


class Tunnel:
    def __init__(self, first_socket: socket.socket, second_socket: socket.socket):
        self.first_socket = first_socket
        self.second_socket = second_socket

    def run(self):
        first_to_second_thread = threading.Thread(target=self.first_to_second)
        second_to_first_thread = threading.Thread(target=self.second_to_first)

        first_to_second_thread.start()
        second_to_first_thread.start()

    def first_to_second(self):
        while True:
            try:
                message = self.first_socket.recv(1024).decode('ascii')
                if message.split(' ')[0] == UDP_PORT_INFO_MESSAGE:
                    (first_udp_socket, first_udp_port) = udp_connection_request_with_port(int(message.split(' ')[1]))
                    udp_tunnel = UDPTunnel(first_udp_socket, first_udp_port, self.second_udp_socket)
                    udp_tunnel.run()
                else:
                    self.second_socket.send(message.encode('ascii'))
            except Exception as e:
                print('Error Happened in Tunnel:', e)
                break

    def second_to_first(self):
        while True:
            try:
                message = self.second_socket.recv(1024).decode('ascii')
                if message == UDP_NEEDED_MESSAGE:

                    self.second_udp_socket = handle_udp_connection_request(self.second_socket)

                    udp_connection_request(self.first_socket, True)


                else:
                    # print(type(self.first_socket), self.first_socket)

                    self.first_socket.send(message.encode('ascii'))
            except Exception as e:
                print('Error Happened in Tunnel:', e)
                break


class UDPTunnel:
    def __init__(self, first_socket: socket.socket, first_port: int, second_socket: socket.socket):
        self.first_socket = first_socket
        self.second_socket = second_socket
        self.first_port = first_port

    def run(self):
        second_to_first_thread = threading.Thread(target=self.second_to_first)
        second_to_first_thread.start()

    def second_to_first(self):
        while True:
            try:
                message = self.second_socket.recvfrom(BUFFER_SIZE)[0]
                self.first_socket.sendto(message, (localhost, self.first_port))
            except Exception as e:
                print('Error Happened in Tunnel:', e)
                break


def connect_and_create_tunnel(client: socket.socket, dest_port: int, message_to_dest: str = None) -> Tunnel:
    socket_to_dest_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_to_dest_server.connect((localhost, dest_port))

    if message_to_dest is not None:
        socket_to_dest_server.send(message_to_dest.encode('ascii'))

    sleep(1.5)
    t = Tunnel(first_socket=client, second_socket=socket_to_dest_server)
    t.run()
    return t

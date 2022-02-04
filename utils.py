import socket
from config import *
from time import sleep


def get_message(client: socket.socket) -> str:
    message = client.recv(1024).decode('ascii')
    return message


def send_message(client: socket.socket, message: str):
    client.send(message.encode('ascii'))


UDP_NEEDED_MESSAGE = '#UDP_NEEDED'
UDP_PORT_INFO_MESSAGE = '#UDP_PORT '
BUFFER_SIZE = 10000000


def udp_connection_request(client: socket.socket):
    send_message(client, UDP_NEEDED_MESSAGE)
    udp_port = int(get_message(client).split()[1])
    sleep(0.5)
    udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_client.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, BUFFER_SIZE)
    return (udp_client, udp_port)


def handle_udp_connection_request(client: socket.socket) -> socket.socket:
    udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_server.bind((localhost, 0))
    port = udp_server.getsockname()[1]
    send_message(client, UDP_PORT_INFO_MESSAGE + str(port))
    return udp_server

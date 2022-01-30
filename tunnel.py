import socket
import threading

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
                self.second_socket.send(message.encode('ascii'))
            except Exception as e:
                print('Error Happened in Tunnel:', e)
                break

    def second_to_first(self):
        while True:
            try:
                message = self.second_socket.recv(1024).decode('ascii')
                self.first_socket.send(message.encode('ascii'))
            except Exception as e:
                print('Error Happened in Tunnel:', e)
                break

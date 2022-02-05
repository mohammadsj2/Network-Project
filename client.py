import pickle
import socket
import threading

import cv2

from config import *
from utils import *


# Init of reading
def read():
    while True:
        try:
            message = get_message(client)
            if message == UDP_NEEDED_MESSAGE:
                handle_stream_thread = threading.Thread(target=handle_stream, args=(client, ))
                handle_stream_thread.start()
            else:
                print(message)
        except:
            break

def handle_stream(client: socket.socket):
    udp_server = handle_udp_connection_request(client)
    while True:
        x = udp_server.recvfrom(BUFFER_SIZE)
        data = x[0]

        if len(data) < 100:
            print(data)
            if data.decode('utf-8') == UDP_STREAMING_FINISH:
                print("DOROST")
                send_message(client, TCP_STREAMING_FINISH)
                break

        data = pickle.loads(data)
        data = cv2.imdecode(data, cv2.IMREAD_COLOR)
        cv2.imshow('Video Streamer (client-side)', data)
        if cv2.waitKey(10) == 13:  # Press Enter then window will close
            send_message(client, TCP_STREAMING_FINISH)
            break
    cv2.destroyAllWindows()

# Init of writing
def write():
    while True:
        message = input()
        try:
            send_message(client, message)
        except:
            client.close()


if __name__ == '__main__':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((localhost, SERVER_PORT))

    thread_read = threading.Thread(target=read)
    thread_write = threading.Thread(target=write)

    thread_read.start()
    thread_write.start()

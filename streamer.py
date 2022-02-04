import socket
import threading
from config import *
from utils import *
import cv2, numpy, pickle

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((localhost, STREAMER_PORT))
server.listen(10)


def stream_video(udp_socket: socket.socket, udp_port: int, video_path: str):
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, photo = cap.read()
        #cv2.imshow('Video Streamer', photo)
        ret, buffer = cv2.imencode(".jpg", photo, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
        x_as_bytes = pickle.dumps(buffer)
        print(len(x_as_bytes))
        udp_socket.sendto(x_as_bytes, (localhost, udp_port))
        if cv2.waitKey(10) == 13:  # Press Enter then window will close
            break
    cv2.destroyAllWindows()
    cap.release()


def menu(client: socket.socket):
    send_message(client, "Welcome to Shalgham.\n")
    l = len(VIDEO_NAMES)
    menu_message = ''
    for i in range(l):
        menu_message += str(i + 1) + ". " + VIDEO_NAMES[i] + "\n"
    menu_message += str(l + 1) + ". Exit\n"
    send_message(client, menu_message)
    while True:
        choice_number = get_message(client)
        try:
            choice_number = int(choice_number)
        except Exception:
            send_message(client, 'Choghondar: Please get a valid number.')
        if choice_number == l + 1:
            send_message(client, 'Choghondar: Bye.')
        elif 1 <= choice_number <= l:
            udp_socket, udp_port = udp_connection_request(client)
            stream_video(udp_socket, udp_port, VIDEO_PATHS[choice_number - 1])
            break
        else:
            send_message(client, 'Choghondar: Please get a valid number.')


def run():
    while True:
        client, address = server.accept()
        print(address)
        read_and_write_thread = threading.Thread(target=menu, args=(client,))
        read_and_write_thread.start()


if __name__ == '__main__':
    run()

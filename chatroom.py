import socket
import re
from threading import Thread
from config import *

BUFFER_SIZE = 4096

ENCODED_MAIN_MENU = '1. Sign Up\n2. Login\n3. Exit'.encode()

CHATTING_WITH_PREFIX = 'CHATTING_WITH:'

MAIN_MENU = 'MAIN_MENU'
SIGN_UP_USERNAME = 'SIGN_UP_USERNAME'
SIGN_UP_PASSWORD = 'SIGN_UP_PASSWORD'
LOGIN_USERNAME = 'LOGIN_USERNAME'
LOGIN_PASSWORD = 'LOGIN_PASSWORD'
INBOX = 'INBOX'

LOAD_REGEX = re.compile(r'load (\d+)')


class MessengerHandler:
    def __init__(self, messenger_socket):
        self.socket = messenger_socket
        self.state = MAIN_MENU
        self.username = None

    def get_inbox(self):
        people = []
        person_number = {}
        msg_cnt = []
        for message in reversed(messages):
            if message[1] == self.username:
                if message[0] not in people:
                    person_number[message[0]] = len(people)
                    people.append(message[0])
                    msg_cnt.append(0)
                if not message[3]:
                    msg_cnt[person_number[message[0]]] += 1
        for user in users_passwords:
            if user != self.username and user not in people:
                people.append(user)
                msg_cnt.append(0)
        inbox_string = ''
        for i in range(len(people)):
            inbox_string += people[i]
            if msg_cnt[i] != 0:
                inbox_string += f' ({msg_cnt[i]})'
            inbox_string += '\n'
        return inbox_string.rstrip('\n')

    def get_messages(self, other_user: str, num: int):
        msg_cnt = 0
        messages_string = ''
        for i in range(len(messages) - 1, -1, -1):
            message = messages[i]
            if (message[1] == self.username and message[0] == other_user) or (
                    message[0] == self.username and message[1] == other_user):
                if message[1] == self.username:
                    messages[i] = (message[0], message[1], message[2], True)
                    if msg_cnt < num:
                        msg_cnt += 1
                        messages_string = f'({message[0]}) {message[2]}\n' + messages_string
                elif msg_cnt < num:
                    msg_cnt += 1
                    messages_string = message[2] + '\n' + messages_string
        return messages_string.rstrip('\n')

    def show_message(self, msg: str):
        self.socket.send(msg.encode())

    def run(self):
        self.socket.send(ENCODED_MAIN_MENU)
        running = True
        while running:
            msg = self.socket.recv(BUFFER_SIZE).decode().rstrip('\n')
            if self.state == MAIN_MENU:
                msg = msg.strip()
                if msg == '1':
                    self.socket.send('Please enter your username.'.encode())
                    self.state = SIGN_UP_USERNAME
                if msg == '2':
                    self.socket.send('Please enter your username'.encode())
                    self.state = LOGIN_USERNAME
                if msg == '3':
                    self.socket.close()
                    running = False
            elif self.state == SIGN_UP_USERNAME:
                if msg in users_passwords or msg.strip() == '0':
                    self.socket.send('This username is already existed or invalid. Please enter another one.'.encode())
                else:
                    self.username = msg
                    self.socket.send('Please enter your password.'.encode())
                    self.state = SIGN_UP_PASSWORD
            elif self.state == SIGN_UP_PASSWORD:  # signup(username, passwd)
                users_passwords[self.username] = msg
                self.username = None
                self.socket.send(ENCODED_MAIN_MENU)
                self.state = MAIN_MENU
            elif self.state == LOGIN_USERNAME:
                self.username = msg
                self.socket.send('Please enter your password.'.encode())
                self.state = LOGIN_PASSWORD
            elif self.state == LOGIN_PASSWORD:  # login(username, passwd)
                if self.username not in users_passwords or users_passwords[self.username] != msg:
                    self.username = None
                    self.socket.send('Incorrect username or password.\n1. Sign Up\n2. Login\n3. Exit'.encode())
                    self.state = MAIN_MENU
                else:
                    if self.username not in users_handlers:
                        users_handlers[self.username] = []
                    if self not in users_handlers[self.username]:
                        users_handlers[self.username].append(self)
                    self.socket.send(self.get_inbox().encode())
                    self.state = INBOX
            elif self.state == INBOX:
                if msg.strip() == '0':
                    users_handlers[self.username].remove(self)
                    self.username = None
                    self.socket.send(ENCODED_MAIN_MENU)
                    self.state = MAIN_MENU
                elif msg != self.username and msg in users_passwords:
                    self.socket.send(self.get_messages(msg, 5).encode())
                    self.state = CHATTING_WITH_PREFIX + msg
            elif self.state.startswith(CHATTING_WITH_PREFIX):
                other_user = self.state[len(CHATTING_WITH_PREFIX):]
                if msg.startswith('/'):
                    msg = msg[1:].rstrip()
                    if msg == 'exit':
                        self.socket.send(self.get_inbox().encode())
                        self.state = INBOX
                    else:
                        match = LOAD_REGEX.fullmatch(msg)
                        if match is not None:
                            num = int(match.group(1))
                            if num > 0:
                                self.socket.send(self.get_messages(other_user, num).encode())
                else:
                    read = False
                    msg_to_show = f'({self.username}) {msg}'
                    if other_user in users_handlers:
                        for handler in users_handlers[other_user]:
                            if handler.state == CHATTING_WITH_PREFIX + self.username:
                                read = True
                                handler.show_message(msg_to_show)
                    messages.append((self.username, other_user, msg, read))


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', CHATROOM_PORT))
server_socket.listen()
print('Messenger server port:', server_socket.getsockname()[1])

users_handlers = {}
users_passwords = {}
messages = []

while True:
    print('Accepting connections')
    (client_socket, client_address) = server_socket.accept()
    new_handler = MessengerHandler(client_socket)
    Thread(target=new_handler.run).start()

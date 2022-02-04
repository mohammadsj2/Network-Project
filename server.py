import socket
import threading
from firewall import Firewall, FirewallType
from config import *
from utils import send_message, get_message
from tunnel import connect_and_create_tunnel

admin_password = None


def init_connection(client: socket.socket, is_first_client: bool = False):
    # After connection of client, server expects the servername [via port] to get connected to.
    global admin_password
    if is_first_client:
        send_message(client, "Set a password for admin user.")
        admin_password = get_message(client)
        send_message(client, "Admin password has been set.")
    send_message(client,
                 "\nChoose one of these options:\n" +
                 "[1] Connect to external servers\n" +
                 "[2] Login as admin")
    query = int(get_message(client))

    if query == 1:
        send_message(client,
                     "input format: (shalgham | choghondar)\n" +
                     "          or: (shalgham | choghondar) via [port]\n" +
                     "Note: shalgham   -> Streamer\n" +
                     "      choghondar -> Chatroom")

        message = get_message(client)
        parts = message.split(' ')
        server_name = parts[0]
        if len(parts) == 1:
            dest_port = server_to_port[server_name]
            server_name = None
        else:
            dest_port = int(parts[2])

        if not firewall.is_valid(dest_port):
            send_message(client, 'packet dropped due to firewall rules')
            print('packet dropped due to firewall rules')
        else:
            t = connect_and_create_tunnel(client, dest_port, server_name)
            tunnels.append(t)
    else:
        send_message(client, 'Enter admin password:')
        password = get_message(client)
        if password != admin_password:
            send_message(client, 'Password is incorrect')
            init_connection(client)
        send_message(client, 'You are logged in as admin.\n Send firewall queries:')
        while True:
            query = get_message(client).split()
            try:
                if query[0] == 'activate':
                    if query[1] == 'whitelist':
                        firewall.set_firewall_type(FirewallType.WHITE_LIST)
                    else:
                        firewall.set_firewall_type(FirewallType.BLACK_LIST)
                elif query[0] == 'open':
                    firewall.open_port(int(query[2]))
                elif query[0] == 'close':
                    firewall.close_port(int(query[2]))
                else:
                    break
            except Exception:
                send_message(client, 'Invalid firewall query.')
        init_connection(client)


def run():
    is_first_client = True
    while True:
        client, address = server.accept()
        print(address)
        init_thread = threading.Thread(target=init_connection, args=(client, is_first_client,))
        is_first_client = False
        init_thread.start()


if __name__ == '__main__':
    firewall = Firewall()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((localhost, SERVER_PORT))
    server.listen(10)
    tunnels = []
    run()

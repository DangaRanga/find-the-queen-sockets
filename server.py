
from http import client
import socket
import datetime as dt
import threading
import ast
import time
import random

# Initialize global variables
PORT = 7621
SERVER_IP = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'
users = []
roles = {
    'dealer': "",
    'spotter': "",
}

user_dict = {
    "1": "",
    "2": ""
}
clients = set()
clients_lock = threading.Lock()


def parse_data(recieved_data):
    try:
        details_eval = ast.literal_eval(recieved_data)
        return details_eval
    except ValueError:
        return "Invalid data inputted"


def validate_login(login_details):
    """Checks if the login details recieved are valid

    Args: 
        <dict> login_details: A dictionary containing the username
         and password of the user attempting to log in

    Returns:
        <bool> True if the user details are valid
            False if they are invalid
    """
    # Initialize valid credentials
    valid_credentials = [
        {
            "username": "dannyboi",
            "password": "dre@margh_shelled"
        },

        {
            "username": "matty7",
            "password": "win&win99"
        }
    ]

    # Check credentials
    for credential in valid_credentials:
        if login_details == credential:
            return (True, login_details.get('username'))

    return (False, '')


def broadcast(msg):
    for client in clients:
        client.send(msg.encode())


def play_game(conn):
    broadcast("Game of Find a Queen has started!")
    get_roles()

    # Send messages to dealer and spotter
    client_lst = list(clients)

    dealer_index = roles['dealer'] - 1
    spotter_index = roles['spotter'] - 1

    client_lst[dealer_index].send('You are the dealer'.encode())
    client_lst[spotter_index].send('You are the spotter'.encode())


def get_roles():
    users_nos = [1, 2]
    role_index = random.choice(users_nos)
    roles['dealer'] = users_nos.pop(0)
    roles['spotter'] = users_nos[0]


def client_handler(conn, addr):
    print(f"[NEW CONNCETION] {addr} connected.")

    connected = True
    # Prompt user to send login details
    conn.send('Please enter your login details'.encode())

    # Retrieve login details
    login_details = conn.recv(1024).decode()

    # Safely evaluate retrieved data
    login_eval = parse_data(login_details)

    # Validate login and check if user isn't already logged in
    login_validity = validate_login(login_eval)

    if(login_validity[0] == False):
        conn.send('[ERROR] Invalid details entered.'.encode())
        conn.close()

    # Check if the user is already logged in
    if(login_validity[1] in users):
        conn.send('[ERROR] User already logged in.')
        conn.close()
        return

    user_dict["1"] = login_validity[1]
    users.append(login_validity[1])

    # Determine dealer and spotter

    while connected:
        if(len(users) == 2):
            play_game(conn)
            break
        else:
            print("Waiting for users to connect")
            time.sleep(100)


def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER_IP}")

    while True:
        conn, addr = server.accept()
        clients.add(conn)
        thread = threading.Thread(
            target=client_handler, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS]{threading.active_count() - 1}")


if __name__ == '__main__':
    print("[STRTING] Server is Starting...")
    run_server()

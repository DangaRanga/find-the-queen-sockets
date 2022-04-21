
import socket
import datetime as dt
import threading
import ast

# Initialize global variables
PORT = 7621
SERVER_IP = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'
users = []


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
            "password": " win&win99"
        }
    ]

    # Check credentials
    for credential in valid_credentials:
        if login_details == credential:
            return (True, login_details.get('username'))

    return (False, '')


def play_game(conn):
    pass


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
        conn.send('Invalid details entered.'.encode())
        conn.close()

    users.append(login_validity[2])

    if(len(users) == 2):
        play_game(conn)

    #  while connected:
    # Recieve login details


def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER_IP}")

    while True:
        if (threading.active_count() - 1 < 2):
            conn, addr = server.accept()

        thread = threading.Thread(
            target=client_handler, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS]{threading.active_count() - 1}")


if __name__ == '__main__':
    print("[STRTING] Server is Starting...")
    run_server()

from calendar import c
from pydoc import cli
import socket

PORT = 7621
HOST = socket.gethostname()


def send_login_details(client_socket):
    # Retrieve initial message from server
    print(client_socket.recv(1024).decode())

    # Accept input for login details
    username = input('Please enter your username -> ')
    password = input('Please enter your password -> ')

    login_details = {
        'username': username,
        'password': password
    }

    # Send details back to server as encoded string
    client_socket.send(str(login_details).encode())


def play_game(client_socket):
    rounds = 5
    for round in range(rounds):
        position = client_socket.recv(1024).decode()

        choice = input("Please select the value 1,2 or 3")
        valid_choices = ['1', '2', '3']
        if choice not in valid_choices:
            print("Invalid choice")

        client_socket.send(choice.encode())

        game_status = client_socket.recv(1024).decode()
        print(game_status)


def run_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    send_login_details(client_socket)

    game_start = client_socket.recv(1024).decode()
    play_game(client_socket)


if __name__ == '__main__':
    run_client()

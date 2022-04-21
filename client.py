from calendar import c
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


def run_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))

        send_login_details(client_socket)


if __name__ == '__main__':
    run_client()


import socket
import datetime as dt
import threading

# Initialize global variables
PORT = 7621
SERVER_IP = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'


def client_handler(conn, addr):
    pass


def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER_IP}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(
            target=client_handler, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS]{threading.active_count() - 1}")


if __name__ == '__main__':
    print("[STRTING] Server is Starting...")
    run_server()

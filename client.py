import socket
import threading
import sys
from prompt_toolkit import print_formatted_text, HTML, prompt

SERVER_ADDRESS = ('localhost', 5001)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(SERVER_ADDRESS)

USERNAME = ""


def send_loop():
    while True:
        try:
            message = prompt("You: ")
            client_socket.send(f"{USERNAME}: {message}".encode('utf-8'))
        except (OSError, KeyboardInterrupt):
            break


def recv_loop():
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                print('\nServer closed the connection.')
                break
            print_formatted_text(HTML(f"<violet>{message.decode('utf-8')}</violet>"))
        except OSError:
            break


if __name__ == '__main__':
    USERNAME = input("Your username?")
    if not USERNAME:
        print("Your username must not be empty.")
        sys.exit()
    recv_thread = threading.Thread(target=recv_loop, daemon=True)
    send_thread = threading.Thread(target=send_loop, daemon=True)
    client_socket.send(f"{USERNAME} joined the chat.".encode("utf-8"))

    recv_thread.start()
    send_thread.start()

    send_thread.join()  # main thread waits here until send_loop exits (e.g. Ctrl+C or error)
    client_socket.send(f"{USERNAME} left the chat".encode('utf-8'))

    client_socket.close()